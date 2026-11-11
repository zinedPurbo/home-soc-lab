"""Self-check for the Discord message format. Run: python3 tests/test_custom_discord.py"""
import importlib.util
import pathlib

path = pathlib.Path(__file__).resolve().parent.parent / "integrations" / "custom-discord.py"
spec = importlib.util.spec_from_file_location("custom_discord", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

full = {
    "timestamp": "2026-11-11T06:30:00Z",
    "agent": {"name": "win11-lab"},
    "rule": {"id": "100100", "level": 10, "description": "PowerShell executed with an encoded command",
             "mitre": {"id": ["T1059.001"]}},
}
msg = mod.build_message(full)
assert "PowerShell executed with an encoded command" in msg
assert "Rule: 100100" in msg and "MITRE: T1059.001" in msg and "Agent: win11-lab" in msg

# Alerts without MITRE or agent info must not crash.
msg = mod.build_message({"rule": {"id": "5710", "level": 5, "description": "sshd: invalid user"}})
assert "MITRE: n/a" in msg and "Agent: unknown" in msg
assert "Wazuh alert" in mod.build_message({})

print("custom-discord: all checks passed")
