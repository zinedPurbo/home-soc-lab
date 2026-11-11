# Home SOC Lab — Threat Detection & Automated Alerting with Wazuh

![Validate detections](https://github.com/zinedPurbo/home-soc-lab/actions/workflows/validate.yml/badge.svg)

A home Security Operations Center built on an Apple Silicon MacBook: a Windows 11 endpoint
instrumented with **Sysmon**, a **Wazuh SIEM** on Ubuntu Server, custom **MITRE ATT&CK**-mapped
detections managed as code, and automated **Discord** alerting.

▶️ **Demo video:** _coming soon_

## Architecture

![Architecture](diagrams/lab-architecture.png)

| Component | Role | Details |
|---|---|---|
| Windows 11 ARM (UTM / QEMU) | Monitored endpoint | Sysmon (SwiftOnSecurity config) + Wazuh agent |
| Ubuntu Server 24.04 ARM (UTM / QEMU) | SIEM | Wazuh 4.14 — manager, indexer, dashboard |
| Discord `#alerts` | Notifications | Custom Wazuh integration, alerts ≥ level 10 |
| GitHub Actions | Detection-as-code | Validates Sigma + Wazuh rules on every push |

Network: UTM Shared Network `192.168.64.0/24` (isolated NAT on the host).

## Detections

| # | Detection | MITRE ATT&CK | Log source | Wazuh rule | Sigma rule | Proof |
|---|---|---|---|---|---|---|
| 01 | PowerShell encoded command | T1059.001 | Sysmon EID 1 | 100100 | [sigma](detections/sigma/01-powershell-encoded-command.yml) | _screenshot_ |
| 02 | Registry Run-key persistence | T1547.001 | Sysmon EID 13 | 100101 | [sigma](detections/sigma/02-registry-run-key.yml) | _screenshot_ |
| 03 | Certutil used to download a file | T1105 | Sysmon EID 1 | 100102 | [sigma](detections/sigma/03-certutil-download.yml) | _screenshot_ |
| 04 | _next detection_ | | | | | |

Full write-ups (test performed, log evidence, false positives, tuning): [docs/detections.md](docs/detections.md)

## Automated alerting

High-severity alerts are pushed to Discord by [`integrations/custom-discord.py`](integrations/custom-discord.py).
The webhook URL lives only in the server's `ossec.conf` and is never committed.

## Skills demonstrated

SIEM (Wazuh) · Sysmon · Windows event logging · Sigma · MITRE ATT&CK · Detection engineering ·
Python · GitHub Actions CI · Linux administration · Virtualization (UTM/QEMU on Apple Silicon)

## Build log & lessons learned

- Ran the whole lab on Apple Silicon (ARM64) — chose ARM builds of Windows 11, Ubuntu, Sysmon (`Sysmon64a.exe`) and Wazuh.
- Diagnosed a VM network split (Apple Virtualization vs QEMU backends land on different NAT subnets) and moved both VMs to QEMU.
- Fixed a black-screen boot by switching the UTM display card from `virtio-gpu-gl-pci` to `virtio-gpu-pci` with OpenGL off.
- Wazuh's generic `4.x` installer URL started returning *Access Denied*; pinned the versioned `4.14` URL and added `curl -f` so a failed download stops instead of executing an error page.
- Rotated a Discord webhook secret after it was exposed in plain text.
- _add more as you go_

## Setup

See [docs/setup.md](docs/setup.md).
