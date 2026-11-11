#!/var/ossec/framework/python/bin/python3
"""Wazuh integration: post alerts to a Discord webhook.

Wazuh calls this with: <alert_file> <api_key> <hook_url>
The hook URL comes from <hook_url> in ossec.conf - it is never stored in this repo.
"""
import json
import os
import ssl
import sys
import urllib.request


def build_message(alert):
    rule = alert.get("rule", {})
    mitre = ", ".join(rule.get("mitre", {}).get("id", [])) or "n/a"
    agent = alert.get("agent", {}).get("name", "unknown")
    return (
        f"**{rule.get('description', 'Wazuh alert')}**\n"
        f"Level: {rule.get('level', '?')} | Rule: {rule.get('id', '?')} | MITRE: {mitre}\n"
        f"Agent: {agent} | Time: {alert.get('timestamp', '?')}"
    )


def main(argv):
    alert_file, hook_url = argv[1], argv[3]
    with open(alert_file) as f:
        alert = json.load(f)
    # Discord caps message content at 2000 characters.
    payload = json.dumps({"content": build_message(alert)[:2000]}).encode()
    req = urllib.request.Request(
        hook_url,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "home-soc-lab-wazuh"},
    )
    # Wazuh's bundled Python has no CA store, so trust the OS bundle (Ubuntu path) when present.
    ca = "/etc/ssl/certs/ca-certificates.crt"
    ctx = ssl.create_default_context(cafile=ca if os.path.exists(ca) else None)
    urllib.request.urlopen(req, timeout=10, context=ctx)


if __name__ == "__main__":
    main(sys.argv)
