#!/usr/bin/env python3
"""Render the "A bit more" highlights as a card.

Everything else on the profile is a generated card now, which left GitHub's
default table styling — plain borders, flat header row — looking out of
place inside this section.
"""

import pathlib

import gh

ROOT = pathlib.Path(__file__).resolve().parent.parent
W = 860
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,monospace"
SANS = "'Segoe UI',Inter,Helvetica,Arial,sans-serif"

# ── "A bit more": lead phrase, supporting detail, accent ──
POINTS = [
    ("Computer Engineering @ KJSSE (SGPA: 9.04)",
     "Building AI/ML and FinTech applications with high academic rigor and production standards.", "#00FF66"),
    ("FinTech & Market Intelligence",
     "MFScope (Mutual Fund Intelligence) & Anomaly Terminal (ML Stock Anomaly Detection).", "#00F0FF"),
    ("AI-Powered FinTech Tools",
     "SwipeRight (AI Credit-Card Recommendation Engine) & FinTrace (Latency Globe).", "#39FF14"),
    ("Full Stack & Dev Tools",
     "PayRozgar (Payroll PWA) & GitControl (Windows Git Desktop App).", "#FFB800"),
    ("Quant & Market Data Visualization",
     "MoneyFlow (Nifty 50 Treemap Heatmap) & Alpha (Pairs Trading Dashboard).", "#FF6B6B"),
    ("Leadership & Ecosystem",
     "Founder of Finance & Technology Club at KJSSE. Lead organizer for FinovateX 2026.", "#A78BFA"),
]


def shell(h, uid, body) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}"
     role="img" aria-label="{uid}">
  <defs>
    <linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{gh.BG0}"/><stop offset="100%" stop-color="{gh.BG1}"/>
    </linearGradient>
    <linearGradient id="ac{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00FF66"/><stop offset="50%" stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#39FF14"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{h}" rx="13" fill="url(#bg{uid})"/>
  <rect x="1" y="1" width="{W - 2}" height="{h - 2}" rx="12" fill="none"
        stroke="url(#ac{uid})" stroke-opacity="0.4" stroke-width="2"/>
{body}
</svg>
'''


def about_list() -> str:
    lead_px, desc_px, desc_lead = 14, 12.5, 17
    rows, y = [], 62
    for i, (lead, desc, colour) in enumerate(POINTS):
        lines = gh.wrap(desc, W - 132, desc_px)
        row_h = 24 + len(lines) * desc_lead + 14
        rows.append(
            f'  <rect x="16" y="{y - 20}" width="{W - 32}" height="{row_h - 6}" rx="8" '
            f'fill="#ffffff" fill-opacity="{0.028 if i % 2 == 0 else 0.008}"/>'
            f'<rect x="26" y="{y - 14}" width="3" height="{row_h - 22}" rx="1.5" fill="{colour}"/>'
            f'<circle cx="27.5" cy="{y - 5}" r="4.5" fill="{colour}">'
            f'<animate attributeName="opacity" values="0.35;1;0.35" dur="3s" '
            f'begin="{i * 0.25:.2f}s" repeatCount="indefinite"/></circle>'
            f'<text x="46" y="{y}" style="font:700 {lead_px}px {SANS};fill:#ffffff">'
            f'{gh.esc(lead)}</text>'
        )
        for j, line in enumerate(lines):
            rows.append(
                f'  <text x="46" y="{y + 22 + j * desc_lead}" '
                f'style="font:400 {desc_px}px {SANS};fill:{gh.MUTED}">{gh.esc(line)}</text>'
            )
        y += row_h

    height = y + 44
    head = (
        f'  <text x="26" y="36" style="font:700 16px {SANS};fill:{gh.TEAL}">◈ A bit more</text>'
        f'<text x="{W - 26}" y="36" text-anchor="end" '
        f'style="font:600 10px {MONO};fill:{gh.DIM};letter-spacing:1.6px">WHAT I ACTUALLY DO</text>'
        f'<line x1="26" y1="46" x2="{W - 26}" y2="46" stroke="{gh.LINE}"/>'
    )
    foot = (
        f'  <line x1="26" y1="{y + 2}" x2="{W - 26}" y2="{y + 2}" stroke="{gh.LINE}"/>'
        f'<text x="26" y="{y + 26}" style="font:600 12.5px {MONO};fill:{gh.TEAL}">'
        f'🌐 jehdadina.xyz</text>'
        f'<text x="{W - 26}" y="{y + 26}" text-anchor="end" '
        f'style="font:400 11.5px {SANS};fill:{gh.MUTED}">Open to collaboration</text>'
    )
    return shell(height, "about-list", head + "\n" + "\n".join(rows) + "\n" + foot)


def main() -> None:
    out = ROOT / "assets"
    out.mkdir(parents=True, exist_ok=True)
    (out / "about-list.svg").write_text(about_list(), encoding="utf-8")
    print("wrote about-list.svg")


if __name__ == "__main__":
    main()
