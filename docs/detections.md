# Detection write-ups

Every test below was run on my own isolated lab VM (`win11-lab`).

<!-- Template for each detection:
## NN – Name (Txxxx)
- **Test:** exact command run on win11-lab
- **Log source:** e.g. Sysmon Event ID 1
- **Rules:** Wazuh 1001xx · sigma/NN-name.yml
- **Result:** fired / did not fire / tuned
- **False positives:** what legit activity could trigger it
- **Evidence:** ![](../screenshots/NN-name.png)
-->

## 01 – PowerShell encoded command (T1059.001)
- **Test:** `powershell -enc VwByAGkAdABlAC0ATwB1AHQAcAB1AHQAIAAiAGgAaQAiAA==` (prints "hi")
- **Log source:** Sysmon Event ID 1 (process create)
- **Rules:** Wazuh 100100 · [sigma](../detections/sigma/01-powershell-encoded-command.yml)
- **Result:** _TODO_
- **False positives:** management tools that pass encoded scripts
- **Evidence:** _TODO screenshot_

## 02 – Registry Run-key persistence (T1547.001)
- **Test:** `reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v LabRun /d notepad.exe /f`
- **Log source:** Sysmon Event ID 13 (registry value set)
- **Rules:** Wazuh 100101 · [sigma](../detections/sigma/02-registry-run-key.yml)
- **Result:** _TODO_
- **False positives:** installers/updaters registering autostart entries
- **Evidence:** _TODO screenshot_
- **Cleanup:** `reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v LabRun /f`

## 03 – Certutil download (T1105)
- **Test:** `certutil -urlcache -f https://example.com C:\Users\Public\test.txt`
- **Log source:** Sysmon Event ID 1
- **Rules:** Wazuh 100102 · [sigma](../detections/sigma/03-certutil-download.yml)
- **Result:** _TODO_ (Defender may also block this — screenshot that too)
- **False positives:** rare admin use
- **Evidence:** _TODO screenshot_
