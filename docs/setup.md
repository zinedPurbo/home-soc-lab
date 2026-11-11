# Setup

Host: MacBook Pro (M1 Pro, 16 GB) running UTM. Both VMs use the **QEMU** backend and **Shared Network**.

| VM | OS | RAM / CPU / Disk | IP |
|---|---|---|---|
| `wazuh-server` | Ubuntu Server 24.04.5 ARM64 | 6 GB / 4 / 60 GB | 192.168.64.4 |
| `win11-lab` | Windows 11 ARM | 4 GB / 2 / — | 192.168.64.x |

## 1. Wazuh server (Ubuntu)

```bash
sudo apt update && sudo apt full-upgrade -y && sudo reboot
curl -fsSO https://packages.wazuh.com/4.14/wazuh-install.sh && sudo bash ./wazuh-install.sh -a
```

Dashboard: `https://192.168.64.4` (user `admin`, password printed by the installer — stored in a password manager).

## 2. Sysmon (Windows, admin PowerShell)

```powershell
cd C:\Tools\Sysmon
.\Sysmon64a.exe -accepteula -i sysmonconfig-export.xml   # ARM64 build + SwiftOnSecurity config
Get-Service Sysmon*
```

## 3. Wazuh agent (Windows)

1. Dashboard → Agents → Deploy new agent → Windows MSI, server `192.168.64.4`, name `win11-lab`; run the generated command.
2. Add [`configs/ossec-agent-sysmon.xml`](../configs/ossec-agent-sysmon.xml) to the agent's `ossec.conf`.
3. `Restart-Service WazuhSvc`

## 4. Custom rules

Copy [`detections/wazuh/local_rules.xml`](../detections/wazuh/local_rules.xml) to `/var/ossec/etc/rules/local_rules.xml`, then:

```bash
sudo /var/ossec/bin/wazuh-analysisd -t && sudo systemctl restart wazuh-manager
```

## 5. Discord alerting

```bash
sudo cp integrations/custom-discord.py /var/ossec/integrations/
sudo chown root:wazuh /var/ossec/integrations/custom-discord.py
sudo chmod 750 /var/ossec/integrations/custom-discord.py
```

Add [`configs/integration-discord.xml`](../configs/integration-discord.xml) to `/var/ossec/etc/ossec.conf` with the real webhook URL, then restart `wazuh-manager`.
