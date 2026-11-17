"""Write identical OpenHands agent_settings.json into each condition's persistence dir.

    python gen_settings.py ROOT [--model openai/qwen3.5:9b]
Only the model differs between models; the Roslyn condition's mcp.json is kept if it exists.

Context budget (SETUP_NOTES.md "Context budget fix"): Ollama serves a 65,536-token window and, when a
prompt does not fit, silently drops the oldest non-system messages (the task first) or cuts the prompt
in half. So OpenHands must condense first, leaving room for the reply:
  prompt <= MAX_INPUT (48,000) and reply <= MAX_OUTPUT (8,192): 56,192 <= 65,536.
The condenser counts only the messages (not the tool schemas sent with every request; 5.7-6.1k tokens
for the Roslyn tool set with gpt-oss), so it triggers at MAX_INPUT - TOOL_SCHEMA_ALLOWANCE. keep_first=2
keeps the system prompt event (system prompt + AGENTS.md) and the task message verbatim."""
import argparse, json, os, sys
from pathlib import Path
from openhands.sdk import LLM
from openhands.sdk.context.condenser import LLMSummarizingCondenser
from openhands_cli.utils import get_default_cli_agent

OLLAMA_CONTEXT = 65536          # OLLAMA_CONTEXT_LENGTH on the Ollama server
MAX_INPUT = 48000               # prompt budget per request
MAX_OUTPUT = 8192               # reply budget per request (sent as max_tokens)
TOOL_SCHEMA_ALLOWANCE = 7000    # tool schemas are not in the condenser's count
CONDENSER_MAX_TOKENS = MAX_INPUT - TOOL_SCHEMA_ALLOWANCE
KEEP_FIRST = 2                  # [SystemPromptEvent, task MessageEvent]
assert MAX_INPUT + MAX_OUTPUT <= OLLAMA_CONTEXT

ap = argparse.ArgumentParser()
ap.add_argument("root")
ap.add_argument("--model", default="openai/qwen3.5:9b")
cli = ap.parse_args()
root = Path(cli.root)
common = dict(
    model=cli.model,
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    temperature=0.0,            # NOTE: not applied by Ollama for gpt-oss (server.log shows temp 1.0); SETUP_NOTES
    max_input_tokens=MAX_INPUT,
    max_output_tokens=MAX_OUTPUT,
    native_tool_calling=True,
    timeout=600,
    num_retries=3,
)
fields = set(LLM.model_fields)
missing = [k for k in common if k not in fields]
assert not missing, f"LLM has no fields {missing}"

llm = LLM(usage_id="agent", **common)
agent = get_default_cli_agent(llm)
condenser = LLMSummarizingCondenser(llm=LLM(usage_id="condenser", **common),
                                    max_tokens=CONDENSER_MAX_TOKENS, keep_first=KEEP_FIRST)
agent = agent.model_copy(update={"condenser": condenser})
spec = agent.model_dump_json(context={"expose_secrets": True}, indent=2)

for cond in ("text", "roslyn"):
    d = root / cond
    d.mkdir(parents=True, exist_ok=True)
    (d / "agent_settings.json").write_text(spec)
    (d / "cli_config.json").write_text(json.dumps({"critic": {"enable_critic": False}}, indent=2))
    mcp = d / "mcp.json"
    if cond == "text" or not mcp.exists():
        mcp.write_text(json.dumps({"mcpServers": {}}, indent=2))
print("wrote", root)
print(json.dumps({k: json.loads(spec)["llm"].get(k) for k in common if k != "api_key"}, indent=1))
print("condenser:", {k: v for k, v in json.loads(spec)["condenser"].items() if k != "llm"})
