#!/usr/bin/env python3
"""Build a unique Matrix Cyber Terminal avatar banner SVG for the profile README.

Self-contained SVG with inlined base64 avatar, animated matrix green particle rings,
live telemetry status meters, and hacker green aesthetic.
"""

import base64
import pathlib
import urllib.request

USER = "jehdadina-jpg"
AVATAR_URL = f"https://github.com/{USER}.png?size=460"
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "avatar-scan.svg"

NODES = [
    ("FINTECH", "#00FF66"),
    ("AI / ML", "#00F0FF"),
    ("AGENTIC AI", "#FFB800"),
    ("FULL STACK", "#39FF14"),
]


def fetch_avatar_data_uri() -> str:
    req = urllib.request.Request(AVATAR_URL, headers={"User-Agent": "readme-builder"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()
    return "data:image/png;base64," + base64.b64encode(raw).decode("ascii")


def build(avatar_uri: str) -> str:
    cx, cy, r = 160, 160, 92

    skill_chips = []
    for i, (label, color) in enumerate(NODES):
        x = 330 + (i % 2) * 165
        y = 196 + (i // 2) * 38
        delay = f"{i * 0.15:.2f}s"
        skill_chips.append(
            f'''    <g opacity="0">
      <animate attributeName="opacity" values="0;1" dur="0.6s" begin="{delay}" fill="freeze"/>
      <rect x="{x}" y="{y}" width="150" height="28" rx="14"
            fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.7" stroke-width="1.2"/>
      <circle cx="{x + 18}" cy="{y + 14}" r="3.5" fill="{color}"/>
      <text x="{x + 30}" y="{y + 18}" class="chip" fill="{color}">{label}</text>
    </g>'''
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 860 320" width="860" height="320" role="img"
     aria-label="Jeh Dadina — Matrix Identity Terminal">
  <title>Jeh Dadina — Matrix Terminal</title>

  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%"   stop-color="#040906"/>
      <stop offset="50%"  stop-color="#09140c"/>
      <stop offset="100%" stop-color="#0d1e13"/>
    </linearGradient>

    <linearGradient id="glow-edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="#00FF66"/>
      <stop offset="50%"  stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#39FF14"/>
    </linearGradient>

    <linearGradient id="title-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="#ffffff"/>
      <stop offset="50%"  stop-color="#00FF66"/>
      <stop offset="100%" stop-color="#00F0FF"/>
    </linearGradient>

    <pattern id="matrix-grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="#00FF66" stroke-opacity="0.08" stroke-width="1"/>
    </pattern>

    <clipPath id="avatar-clip">
      <circle cx="{cx}" cy="{cy}" r="{r}"/>
    </clipPath>

    <filter id="soft-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <style>
      .title {{ font-family: "Segoe UI",Inter,Helvetica,sans-serif;
                font-size: 38px; font-weight: 800; fill: url(#title-grad); letter-spacing: -0.5px; }}
      .sub   {{ font-family: "JetBrains Mono",Consolas,monospace;
                font-size: 12px; font-weight: 700; fill: #00FF66; letter-spacing: 2.2px; }}
      .mono  {{ font-family: "JetBrains Mono",Consolas,monospace;
                font-size: 12.5px; fill: #629E75; }}
      .chip  {{ font-family: "JetBrains Mono",Consolas,monospace;
                font-size: 11px; font-weight: 700; letter-spacing: 1px; }}
      .tag   {{ font-family: "JetBrains Mono",Consolas,monospace;
                font-size: 9.5px; font-weight: 700; fill: #00FF66; letter-spacing: 1.5px; }}
    </style>
  </defs>

  <rect width="860" height="320" rx="16" fill="url(#bg)"/>
  <rect width="860" height="320" rx="16" fill="url(#matrix-grid)"/>

  <!-- Left: Avatar Hologram Frame -->
  <g>
    <!-- Outer Orbit Rings with Rotation Animation -->
    <circle cx="{cx}" cy="{cy}" r="{r + 20}" fill="none" stroke="#00FF66" stroke-opacity="0.25"
            stroke-width="1.5" stroke-dasharray="4 12">
      <animateTransform attributeName="transform" type="rotate"
                        from="360 {cx} {cy}" to="0 {cx} {cy}" dur="25s" repeatCount="indefinite"/>
    </circle>

    <circle cx="{cx}" cy="{cy}" r="{r + 12}" fill="none" stroke="#00F0FF" stroke-opacity="0.45"
            stroke-width="1.8" stroke-dasharray="24 16 8 16">
      <animateTransform attributeName="transform" type="rotate"
                        from="0 {cx} {cy}" to="360 {cx} {cy}" dur="18s" repeatCount="indefinite"/>
    </circle>

    <!-- Avatar Image -->
    <image xlink:href="{avatar_uri}" x="{cx - r}" y="{cy - r}" width="{r * 2}" height="{r * 2}"
           clip-path="url(#avatar-clip)" preserveAspectRatio="xMidYMid slice"/>

    <!-- Gradient Ring around Avatar -->
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#glow-edge)" stroke-width="2.5" filter="url(#soft-glow)"/>

    <!-- Pulse LED Status Badge -->
    <rect x="{cx - 54}" y="{cy + r - 14}" width="108" height="22" rx="11" fill="#040906" stroke="#00FF66" stroke-opacity="0.7" stroke-width="1.2"/>
    <circle cx="{cx - 38}" cy="{cy + r - 3}" r="3.5" fill="#00FF66">
      <animate attributeName="opacity" values="1;0.2;1" dur="1.8s" repeatCount="indefinite"/>
    </circle>
    <text x="{cx + 6}" y="{cy + r + 1}" text-anchor="middle" class="tag">ROOT · ACTIVE</text>
  </g>

  <!-- Right: Identity & Telemetry Panel -->
  <g transform="translate(330, 48)">
    <text x="0" y="24" class="title">Jeh Dadina</text>
    <text x="0" y="48" class="sub">COMPUTER ENGINEERING · AI/ML × FINTECH</text>

    <!-- Terminal Box -->
    <rect x="0" y="66" width="490" height="66" rx="8" fill="#030704" fill-opacity="0.8" stroke="#1a3824" stroke-width="1"/>
    <text x="16" y="90" class="mono"><tspan fill="#00FF66">&gt;</tspan> <tspan fill="#E0F8E8">INSTITUTION:</tspan> KJ Somaiya School of Engineering</text>
    <text x="16" y="112" class="mono"><tspan fill="#00FF66">&gt;</tspan> <tspan fill="#E0F8E8">CURRENT SGPA:</tspan> <tspan fill="#FFB800" font-weight="700">9.04</tspan> | <tspan fill="#E0F8E8">FOUNDER @</tspan> FinTech Club</text>
  </g>

  <!-- Skill Pill Cards -->
{chr(10).join(skill_chips)}

  <!-- Animated Bottom Matrix Line -->
  <rect x="330" y="278" width="490" height="2" rx="1" fill="#00FF66" fill-opacity="0.15"/>
  <rect y="278" width="100" height="2" rx="1" fill="url(#glow-edge)">
    <animate attributeName="x" values="330;720;330" dur="4s" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" repeatCount="indefinite"/>
  </rect>

  <!-- Outer Card Gradient Frame -->
  <rect x="1" y="1" width="858" height="318" rx="15" fill="none" stroke="url(#glow-edge)" stroke-opacity="0.5" stroke-width="1.8"/>
</svg>
'''


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(fetch_avatar_data_uri()), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
