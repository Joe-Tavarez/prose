"""Run one OpenHands conversation headlessly, with an explicit step limit.

Runs with the pinned OpenHands CLI environment's Python (uv tool `openhands==1.16.0`, SDK 1.21.0).
The agent is built exactly as the CLI builds it, by `openhands_cli.setup.load_agent_specs`, from
OPENHANDS_PERSISTENCE_DIR: LLM + condenser from agent_settings.json, the CLI's default tools,
MCP servers from mcp.json, and project skills (a root AGENTS.md is loaded as an always-on skill).
The conversation is set up like the CLI's (LLM security analyzer, hooks, builtin subagents) with
NeverConfirm, as `--headless` does. What differs from `openhands --headless`: the step limit is
explicit (the CLI always uses the SDK default of 500), and every event is written to a JSONL file.

    python oh_driver.py --workdir REPO --task-file task.md --events events.jsonl --summary run.json
    python oh_driver.py --workdir REPO --dry-run --summary dry.json   # build agent, list tools, no LLM calls
"""
import argparse
import asyncio
import json
import os
import re
import sys
import time
import uuid


def mcp_check(mcp_config: dict) -> dict:
    """Connect to each configured MCP server, list its tools, and call roslyn_health if present."""
    from fastmcp import Client

    async def check(name, server):
        url = server.get("url") if isinstance(server, dict) else getattr(server, "url", None)
        out = {"url": url}
        try:
            async with Client(url) as client:
                tools = await client.list_tools()
                out["tools"] = sorted(t.name for t in tools)
                if "roslyn_health" in out["tools"]:
                    result = await client.call_tool("roslyn_health", {})
                    text = "".join(getattr(c, "text", "") for c in result.content)
                    health = json.loads(text)
                    out["health"] = {k: health.get(k) for k in (
                        "status", "solutionPath", "projectCount", "documentCount",
                        "workspaceDiagnosticCount", "warnings")}
        except Exception as ex:  # report, don't crash the dry run
            out["error"] = f"{type(ex).__name__}: {ex}"
        return name, out

    async def run_all():
        servers = (mcp_config or {}).get("mcpServers", {})
        return dict(await asyncio.gather(*(check(n, s) for n, s in servers.items())))

    return asyncio.run(run_all())


FILE_EDIT_COMMANDS = {"create", "str_replace", "insert", "undo_edit"}
GATE_MESSAGES = {  # decided 2026-11-15 (SETUP_NOTES.md "Pre-run design decisions")
    "roslyn": "Call roslyn_diagnostics on your changed files before finishing. "
              "If it reports errors, fix the errors you introduced.",
    "text": "Run dotnet build before finishing. If dotnet build fails, fix the errors you introduced.",
}
# Ollama answers HTTP 500 when the model's tool call isn't valid JSON ("error parsing tool call");
# litellm raises after its retries and the SDK ends the run. We tell the model and continue instead.
MALFORMED_MESSAGE = "Your tool call was malformed; try again with valid arguments."
MALFORMED_RE = re.compile(r"error parsing tool call|failed to parse tool call|invalid tool call", re.I)


class FinishGate:
    """Stop hook: the first time the agent finishes without the condition's check after its last
    file edit, refuse the stop once and send GATE_MESSAGES[condition]. Uses the SDK's own stop-hook
    path (LocalConversation.run -> _hook_processor.run_stop), so the agent continues in the same
    run loop and the same max_iteration_per_run budget. Wraps any configured hook processor."""

    def __init__(self, condition, inner=None):
        self.condition, self.inner = condition, inner
        self.actions = 0
        self.last_edit = None   # action number of the last file_editor edit
        self.last_check = None  # action number of the last required check
        self.record = {"condition": condition, "message": GATE_MESSAGES[condition], "triggered": False,
                       "triggeredAtAction": None, "reason": None, "checkAfterGate": False,
                       "finishedAgainWithoutCheck": False}

    def is_check(self, tool, action):
        if self.condition == "roslyn":
            return tool == "roslyn_diagnostics"
        command = str(getattr(action, "command", "") or "")
        return tool == "terminal" and ("dotnet build" in command or "dotnet test" in command)

    def on_action(self, event):
        self.actions += 1
        tool, action = getattr(event, "tool_name", None), getattr(event, "action", None)
        if tool == "file_editor" and getattr(action, "command", None) in FILE_EDIT_COMMANDS:
            self.last_edit = self.actions
        if self.is_check(tool, action):
            self.last_check = self.actions
            if self.record["triggered"]:
                self.record["checkAfterGate"] = True

    def needs_check(self):
        if self.last_check is None:
            return "no check at all"
        if self.last_edit is not None and self.last_check < self.last_edit:
            return "no check after the last edit"
        return None

    def run_stop(self, reason=None):
        if self.inner is not None:
            should_stop, feedback = self.inner.run_stop(reason)
            if not should_stop:
                return should_stop, feedback
        missing = self.needs_check()
        if missing and not self.record["triggered"]:
            self.record.update(triggered=True, triggeredAtAction=self.actions, reason=missing)
            return False, GATE_MESSAGES[self.condition]
        if missing:
            self.record["finishedAgainWithoutCheck"] = True
        return True, None

    def run_session_end(self):
        if self.inner is not None:
            self.inner.run_session_end()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workdir", required=True, help="repository checkout the agent works in")
    ap.add_argument("--task-file", help="prompt (required unless --dry-run)")
    ap.add_argument("--events", help="JSONL file for every conversation event")
    ap.add_argument("--summary", required=True, help="JSON file for the run summary")
    ap.add_argument("--max-steps", type=int, default=100, help="max_iteration_per_run")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--finish-gate", choices=("roslyn", "text", "off"), default="off",
                    help="send the agent back once if it finishes without the condition's check")
    args = ap.parse_args()

    workdir = os.path.abspath(args.workdir)
    os.environ["OPENHANDS_WORK_DIR"] = workdir  # read by the CLI's agent context (AGENTS.md, cwd note)
    os.environ.setdefault("OPENHANDS_SUPPRESS_BANNER", "1")
    os.chdir(workdir)

    from openhands.sdk import AgentContext, Conversation, Workspace
    from openhands.sdk.hooks import HookConfig
    from openhands.sdk.security.confirmation_policy import NeverConfirm
    from openhands.sdk.security.llm_analyzer import LLMSecurityAnalyzer
    from openhands.tools.preset.default import register_builtins_agents
    from openhands_cli.locations import get_conversations_dir, get_persistence_dir
    from openhands_cli.setup import load_agent_specs
    from openhands_cli.stores import agent_store

    # Public skills OFF (both conditions). The CLI builds the agent context with
    # load_public_skills=True, which clones github.com/OpenHands/extensions at its latest commit
    # and adds ~73 skills to the prompt: unpinned (not reproducible) and context a 9B model needs.
    # This is AgentStore._build_agent_context from openhands-cli 1.16.0 with only that flag changed.
    def _agent_context_without_public_skills(self):
        work_dir = agent_store.get_work_dir()
        return AgentContext(
            skills=agent_store.load_project_skills(work_dir),
            system_message_suffix="\n".join([
                f"Your current working directory is: {work_dir}",
                f"User operating system: {agent_store.get_os_description()}",
            ]),
            load_user_skills=True,
            load_public_skills=False,
        )

    agent_store.AgentStore._build_agent_context = _agent_context_without_public_skills

    conversation_id = uuid.uuid4()
    register_builtins_agents(enable_browser=False)
    agent = load_agent_specs(str(conversation_id), critic_disabled=True)

    skills = agent.agent_context.skills if agent.agent_context else []
    summary = {
        "persistenceDir": get_persistence_dir(),
        "workdir": workdir,
        "conversationId": str(conversation_id),
        "maxSteps": args.max_steps,
        "model": agent.llm.model,
        "baseUrl": agent.llm.base_url,
        "tools": [t.name for t in agent.tools],
        "mcpServers": sorted((agent.mcp_config or {}).get("mcpServers", {})),
        "skills": [s.name for s in skills],  # project (AGENTS.md -> "agents") + user skills; public skills are off
        "publicSkills": bool(agent.agent_context and agent.agent_context.load_public_skills),
        "critic": agent.critic is not None,
    }

    if args.dry_run:
        summary["mcpCheck"] = mcp_check(agent.mcp_config)
        with open(args.summary, "w", encoding="utf8") as f:
            json.dump(summary, f, indent=2)
        print(json.dumps(summary, indent=2))
        return 0

    if not args.task_file or not args.events:
        ap.error("--task-file and --events are required unless --dry-run")
    task = open(args.task_file, encoding="utf8").read()

    events = open(args.events, "w", encoding="utf8")
    counts = {"actions": 0, "toolCalls": {}, "agentErrors": 0, "condensations": 0}
    gate = FinishGate(args.finish_gate) if args.finish_gate != "off" else None

    def on_event(event):
        kind = type(event).__name__
        try:
            line = event.model_dump_json()
        except Exception:
            line = json.dumps({"kind": kind, "repr": repr(event)[:2000]})
        events.write(line + "\n")
        events.flush()
        if kind == "ActionEvent":
            counts["actions"] += 1
            name = getattr(event, "tool_name", None) or "?"
            counts["toolCalls"][name] = counts["toolCalls"].get(name, 0) + 1
            if gate is not None:
                gate.on_action(event)
        elif kind == "AgentErrorEvent":
            counts["agentErrors"] += 1
        elif kind == "Condensation":
            counts["condensations"] += 1

    conversation = Conversation(
        agent=agent,
        workspace=Workspace(working_dir=workdir),
        persistence_dir=get_conversations_dir(),
        conversation_id=conversation_id,
        callbacks=[on_event],
        hook_config=HookConfig.load(working_dir=workdir),
        max_iteration_per_run=args.max_steps,
        visualizer=None,
    )
    conversation.set_security_analyzer(LLMSecurityAnalyzer())
    conversation.set_confirmation_policy(NeverConfirm())

    # Count model turns ourselves (every agent.step, including one that fails on an unparseable tool
    # call), so recovering from a malformed call never grants extra turns: the whole conversation gets
    # at most --max-steps turns, exactly like one uninterrupted run.
    turns = {"n": 0}
    agent_cls = type(agent)
    original_step = agent_cls.step

    def counted_step(self, *a, **kw):
        turns["n"] += 1
        return original_step(self, *a, **kw)

    agent_cls.step = counted_step
    counts["malformedToolCalls"] = 0

    started = time.time()
    error = None
    try:
        conversation.send_message(task)
        conversation._ensure_agent_ready()
        if gate is not None:
            # The hook processor is created when the agent is first readied; install the gate around
            # it (or alone, when no hooks are configured) before the run loop starts.
            gate.inner = conversation._hook_processor
            conversation._hook_processor = gate
        while True:
            try:
                conversation.run()
                break
            except Exception as ex:
                remaining = args.max_steps - turns["n"]
                if not MALFORMED_RE.search(str(ex)) or remaining <= 0:
                    raise
                # Same handling in both conditions: tell the model, count it, continue in the budget left.
                counts["malformedToolCalls"] += 1
                print(f"malformed tool call #{counts['malformedToolCalls']} at turn {turns['n']}; "
                      f"continuing with {remaining} turns left", flush=True)
                conversation.max_iteration_per_run = remaining
                conversation.send_message(MALFORMED_MESSAGE)
    except Exception as ex:
        error = f"{type(ex).__name__}: {ex}"
    finally:
        events.close()

    state = conversation.state
    metrics = None
    try:
        combined = conversation.conversation_stats.get_combined_metrics()
        usage = combined.accumulated_token_usage
        metrics = {"promptTokens": usage.prompt_tokens, "completionTokens": usage.completion_tokens}
    except Exception:
        pass
    summary.update({
        "status": str(getattr(state.execution_status, "value", state.execution_status)),
        "hitStepLimit": counts["actions"] >= args.max_steps,
        "seconds": round(time.time() - started, 1),
        "error": error,
        "tokens": metrics,
        "finishGate": gate.record if gate is not None else None,
        "modelTurns": turns["n"],
        **counts,
    })
    with open(args.summary, "w", encoding="utf8") as f:
        json.dump(summary, f, indent=2)
    return 0 if error is None else 1


if __name__ == "__main__":
    sys.exit(main())
