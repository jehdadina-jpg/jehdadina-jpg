#!/usr/bin/env python3
"""Render each featured project as its own card SVG.

Each project gets a distinct, vibrant accent color, tech chips, and custom styling.
"""

import pathlib
import gh

OUT_DIR = pathlib.Path(__file__).resolve().parent.parent / "assets" / "cards"
W, H = 424, 208

# slug, display title, language, [chips], description, live?, custom_accent_color
PROJECTS = [
    ("mf-scope", "MF Scope", "Python", ["Finance", "Data Analysis"],
     "Comprehensive mutual fund analysis platform for the Indian market — data-driven insights "
     "for investment research and financial decision-making.", False, "#00FF66"),
    ("anomaly-terminal", "Anomaly Terminal", "Python", ["ML", "Finance"],
     "Bloomberg-inspired stock market analysis platform combining technical analysis with machine learning "
     "to detect unusual market behavior and generate AI-powered trading recommendations.", False, "#00F0FF"),
    ("sahayak", "sahayAK", "Python", ["NLP", "Voice", "AI"],
     "AI-powered multilingual voice assistant for Indian bank branch desks — NLP capabilities and "
     "regional language support to enhance customer service and accessibility.", False, "#39FF14"),
    ("payrozgar", "PayRozgar", "JavaScript", ["React", "Node.js", "FinTech"],
     "One-tap salary and attendance tracker for small-scale Indian retail shops — automated wage-advance "
     "ledgers and instant salary slip generation.", False, "#FFB800"),
]


def build(slug, title, lang, chips, desc, live, stars, colour) -> str:
    lines = gh.wrap(desc, W - 56, 12.5)[:4]
    body = "\n".join(
        f'    <text x="26" y="{112 + i * 18}" class="d-{slug}">{gh.esc(t)}</text>'
        for i, t in enumerate(lines)
    )

    chip_parts, x = [], 26
    for chip in chips:
        cw = len(chip) * 6.6 + 20
        chip_parts.append(
            f'    <rect x="{x}" y="{H - 42}" width="{cw:.0f}" height="22" rx="11" '
            f'fill="{colour}" fill-opacity="0.12" stroke="{colour}" stroke-opacity="0.45"/>\n'
            f'    <text x="{x + cw / 2:.0f}" y="{H - 27}" class="c-{slug}" '
            f'text-anchor="middle">{gh.esc(chip)}</text>'
        )
        x += cw + 8

    star_block = ""
    if stars:
        star_block = (
            f'  <path d="M{W - 74} 30 l3.2 6.6 7.2 1-5.2 5.1 1.2 7.2-6.4-3.4-6.4 3.4 '
            f'1.2-7.2-5.2-5.1 7.2-1z" fill="{gh.AMBER}" opacity="0.95"/>\n'
            f'  <text x="{W - 26}" y="42" class="s-{slug}" text-anchor="end">{stars}</text>'
        )

    live_block = ""
    if live:
        live_block = (
            f'  <circle cx="{W - 30}" cy="{H - 31}" r="4" fill="{gh.TEAL}">\n'
            f'    <animate attributeName="opacity" values="1;0.25;1" dur="2.2s" '
            f'repeatCount="indefinite"/>\n  </circle>\n'
            f'  <text x="{W - 40}" y="{H - 27}" class="l-{slug}" text-anchor="end">LIVE</text>'
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


def fetch_stars() -> dict[str, int]:
    try:
        repos = gh.api(f"users/{gh.USER}/repos?per_page=100")
        return {r["name"].lower(): r["stargazers_count"] for r in repos if isinstance(r, dict)}
    except Exception:
        return {}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stars = fetch_stars()
    for slug, title, lang, chips, desc, live, colour in PROJECTS:
        s_count = stars.get(slug.lower(), 0)
        svg = build(slug, title, lang, chips, desc, live, s_count, colour)
        path = OUT_DIR / f"{slug}.svg"
        path.write_text(svg, encoding="utf-8")
        print(f"wrote {path.name} (stars={s_count})")


if __name__ == "__main__":
    main()
