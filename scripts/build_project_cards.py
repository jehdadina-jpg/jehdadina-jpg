#!/usr/bin/env python3
"""Render each featured project as its own card SVG.

Each project gets a distinct, vibrant accent color, tech chips, and custom styling.
"""

import pathlib
import gh

OUT_DIR = pathlib.Path(__file__).resolve().parent.parent / "assets" / "cards"
W = 424  # card height is derived per-project from how many lines its description wraps to

# slug, display title, language, [chips], description, live?, custom_accent_color, repo (owner/name, for stars)
PROJECTS = [
    ("anomaly-terminal", "Anomaly Terminal", "Python", ["ML", "Finance"],
     "Bloomberg-inspired stock market analysis platform combining technical analysis with ML to detect "
     "unusual market behavior and generate AI-powered Buy, Hold, and Sell recommendations.",
     False, "#00F0FF", "jehdadina-jpg/anomaly"),
    ("payrozgar", "PayRozgar", "HTML", ["PWA", "Vanilla JS", "FinTech"],
     "Offline-first payroll & attendance PWA for small shops — vanilla JS state engine, service-worker "
     "caching, and auto-generated digital payslips. Built under FTC KJSSE.",
     False, "#FFB800", "FTC-KJSSE/payrozgar"),
    ("mf-scope", "MFScope", "Python", ["FastAPI", "React", "Data"],
     "India mutual fund intelligence engine — pulls daily AMFI NAV data, engineers 30+ risk/sentiment "
     "features, and scores funds Strong Buy → Strong Sell via a FastAPI + React dashboard.",
     False, "#00FF66", "jehdadina-jpg/MFScope"),
    ("swiperight", "SwipeRight", "Python", ["Next.js", "ML", "FinTech"],
     "AI credit-card recommendation engine — parses bank statements, ML-categorizes spend across 13 "
     "categories, and returns the one best card from 140+ Indian cards with an AI chat to explain why.",
     False, "#FF3EA5", "jehdadina-jpg/swiperight"),
    ("fintrace", "FinTrace", "JavaScript", ["Node.js", "Real-Time", "FinTech"],
     "Live network-latency globe for financial infrastructure — traceroutes to NSE, NYSE, Binance, and "
     "AWS regions, streamed via SSE onto a 3D rotating globe with a Bloomberg-terminal readout.",
     False, "#3572A5", "FTC-KJSSE/fintrace"),
    ("gitcontrol", "GitControl", "TypeScript", ["Electron", "Git", "Desktop"],
     "A premium Windows desktop app for visually driving Git and GitHub from one place — no manual "
     "shell commands required for everyday workflows.",
     False, "#58A6FF", "jehdadina-jpg/GitControl"),
    ("moneyflow", "MoneyFlow", "Python", ["FastAPI", "D3.js", "Real-Time"],
     "Live Bloomberg-terminal-style treemap heatmap for the Nifty 50 — FastAPI + yfinance backend "
     "streaming real-time market data onto a D3.js frontend.",
     False, "#A78BFA", "jehdadina-jpg/moneyflow"),
    ("alpha", "Alpha", "Python", ["FastAPI", "Quant", "Python"],
     "Terminal-style dashboard for NSE stocks — a cointegrated pairs scanner, realized volatility "
     "term structure, and a factor exposure grid, built on FastAPI and yfinance.",
     False, "#FF8C42", "jehdadina-jpg/alpha"),
]


def build(slug, title, lang, chips, desc, live, stars, colour) -> str:
    lines = gh.wrap(desc, W - 56, 12.5)[:5]
    body = "\n".join(
        f'    <text x="26" y="{112 + i * 18}" class="d-{slug}">{gh.esc(t)}</text>'
        for i, t in enumerate(lines)
    )

    # Chip row sits below however many lines the description actually wrapped
    # to — a fixed offset here is what let long descriptions collide with it.
    chip_top = 112 + len(lines) * 18
    H = chip_top + 42

    chip_parts, x = [], 26
    for chip in chips:
        cw = len(chip) * 6.6 + 20
        chip_parts.append(
            f'    <rect x="{x}" y="{chip_top}" width="{cw:.0f}" height="22" rx="11" '
            f'fill="{colour}" fill-opacity="0.12" stroke="{colour}" stroke-opacity="0.45"/>\n'
            f'    <text x="{x + cw / 2:.0f}" y="{chip_top + 15}" class="c-{slug}" '
            f'text-anchor="middle">{gh.esc(chip)}</text>'
        )
        x += cw + 8

    star_block = ""
    if stars:
        star_block = (
            f'  <path d="M{W - 52} 33 l2.6 5.4 5.9.9-4.3 4.1 1 5.9-5.2-2.8-5.2 2.8 '
            f'1-5.9-4.3-4.1 5.9-.9z" fill="{gh.AMBER}" opacity="0.95"/>\n'
            f'  <text x="{W - 26}" y="42" class="s-{slug}" text-anchor="end">{stars}</text>'
        )

    live_block = ""
    if live:
        live_block = (
            f'  <circle cx="{W - 30}" cy="{chip_top + 11}" r="4" fill="{gh.TEAL}">\n'
            f'    <animate attributeName="opacity" values="1;0.25;1" dur="2.2s" '
            f'repeatCount="indefinite"/>\n  </circle>\n'
            f'  <text x="{W - 40}" y="{chip_top + 15}" class="l-{slug}" text-anchor="end">LIVE</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"
     role="img" aria-label="{gh.esc(title)} — {gh.esc(lang)} project">
  <title>{gh.esc(title)}</title>
  <defs>
    <linearGradient id="bg-{slug}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{gh.BG0}"/><stop offset="100%" stop-color="{gh.BG1}"/>
    </linearGradient>
    <linearGradient id="top-{slug}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{colour}"/>
      <stop offset="100%" stop-color="{colour}" stop-opacity="0.05"/>
    </linearGradient>
    <style>
      .t-{slug} {{ font-family:"Segoe UI",Inter,Helvetica,sans-serif; font-size:17px;
                   font-weight:700; fill:#ffffff; }}
      .g-{slug} {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:10.5px;
                   fill:{colour}; letter-spacing:0.6px; }}
      .d-{slug} {{ font-family:"Segoe UI",Inter,Helvetica,sans-serif; font-size:12.5px;
                   fill:{gh.MUTED}; }}
      .c-{slug} {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:10px;
                   font-weight:600; fill:{colour}; }}
      .s-{slug} {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:12.5px;
                   font-weight:700; fill:{gh.AMBER}; }}
      .l-{slug} {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:9.5px;
                   font-weight:700; fill:{gh.TEAL}; letter-spacing:1.2px; }}
    </style>
  </defs>

  <rect width="{W}" height="{H}" rx="14" fill="url(#bg-{slug})"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="13" fill="none"
        stroke="{colour}" stroke-opacity="0.45" stroke-width="1.8"/>

  <!-- Top Accent Bar -->
  <rect x="1" y="1" width="{W - 2}" height="3" rx="1.5" fill="url(#top-{slug})"/>

  <!-- Title & Language Dot -->
  <circle cx="34" cy="38" r="6" fill="{colour}"/>
  <text x="50" y="43" class="t-{slug}">{gh.esc(title)}</text>
  <text x="50" y="62" class="g-{slug}">{gh.esc(lang).upper()}</text>

{star_block}
{body}
{"".join(chip_parts)}
{live_block}
</svg>
'''


def fetch_stars(repo: str) -> int:
    try:
        return gh.api(f"repos/{repo}").get("stargazers_count", 0)
    except Exception:
        return 0


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for slug, title, lang, chips, desc, live, colour, repo in PROJECTS:
        s_count = fetch_stars(repo)
        svg = build(slug, title, lang, chips, desc, live, s_count, colour)
        path = OUT_DIR / f"{slug}.svg"
        path.write_text(svg, encoding="utf-8")
        print(f"wrote {path.name} (stars={s_count})")


if __name__ == "__main__":
    main()
