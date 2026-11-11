"""Regenerate diagrams/lab-architecture.png:  python3 diagrams/make_diagram.py"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(13, 6.6), dpi=150)
ax.set_xlim(0, 13); ax.set_ylim(0, 6.6); ax.axis("off")
INK, MUTED = "#1f2933", "#52606d"

def box(x, y, w, h, title, lines, fill, edge):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.15",
                                fc=fill, ec=edge, lw=1.8))
    ax.text(x + w / 2, y + h - 0.32, title, ha="center", va="top", fontsize=12.5, weight="bold", color=INK)
    for i, t in enumerate(lines):
        ax.text(x + w / 2, y + h - 0.85 - i * 0.36, t, ha="center", va="top", fontsize=9.6, color=MUTED)

def arrow(a, b, label, dy=0.18):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=18, lw=1.8, color=INK))
    ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + dy, label, ha="center", fontsize=9.2, color=INK,
            bbox=dict(fc="white", ec="none", pad=1.5))

# Host frame
ax.add_patch(FancyBboxPatch((0.2, 0.25), 9.15, 5.75, boxstyle="round,pad=0.02,rounding_size=0.2",
                            fc="#f5f7fa", ec="#9aa5b1", lw=1.2, ls="--"))
ax.text(0.45, 5.78, "MacBook Pro M1 Pro  ·  UTM (QEMU)  ·  Shared Network 192.168.64.0/24",
        fontsize=10, color=MUTED, va="top")

box(0.55, 1.3, 3.6, 3.9, "Windows 11 ARM", ["windows-11-lab  ·  192.168.64.2", "",
    "Sysmon64a", "(SwiftOnSecurity config)", "", "Wazuh agent 4.14"], "#e3f0ff", "#2f6fdf")
box(5.4, 1.3, 3.6, 3.9, "Ubuntu Server 24.04 ARM", ["wazuh-server  ·  192.168.64.4", "",
    "Wazuh manager + custom rules", "100100-100102 detections", "100110-100111 tuning",
    "Wazuh indexer + dashboard", "custom-discord.py integration"], "#e6f6ec", "#2f9e5b")
box(10.0, 3.45, 2.75, 1.75, "Discord #alerts", ["alerts level >= 10", "via webhook (HTTPS)"], "#efeafd", "#6b4fd8")
box(10.0, 0.6, 2.75, 1.75, "GitHub Actions", ["validates Sigma +", "Wazuh rules on push"], "#fff4e0", "#d98a00")

arrow((4.15, 3.25), (5.4, 3.25), "events\n1514/tcp", dy=0.12)
arrow((9.0, 4.3), (10.0, 4.3), "alerts")
ax.text(7.2, 0.55, "Analyst: dashboard https://192.168.64.4", ha="center", fontsize=9.2, color=MUTED)
ax.text(11.37, 0.3, "detection-as-code (this repo)", ha="center", fontsize=8.6, color=MUTED)

fig.savefig("diagrams/lab-architecture.png", bbox_inches="tight", facecolor="white")
