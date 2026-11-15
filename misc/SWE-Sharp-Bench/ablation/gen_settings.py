"""Write identical OpenHands agent_settings.json into each condition's persistence dir."""
import json, os, sys
from pathlib import Path
from openhands.sdk import LLM
from openhands.sdk.context.condenser import LLMSummarizingCondenser
from openhands_cli.utils import get_default_cli_agent

root = Path(sys.argv[1])
common = dict(
    model="openai/qwen3.5:9b",
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    temperature=0.0,
    max_input_tokens=65536,
    max_output_tokens=8192,
    native_tool_calling=True,
    timeout=600,
    num_retries=3,
)
fields = set(LLM.model_fields)
missing = [k for k in common if k not in fields]
assert not missing, f"LLM has no fields {missing}"

llm = LLM(usage_id="agent", **common)
agent = get_default_cli_agent(llm)
agent = agent.model_copy(update={"condenser": LLMSummarizingCondenser(llm=LLM(usage_id="condenser", **common))})
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
