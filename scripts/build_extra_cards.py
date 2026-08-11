#!/usr/bin/env python3
"""Render the two remaining markdown tables as cards.

Everything else on the profile is a generated card now, which left GitHub's
default table styling — plain borders, flat header row — looking out of place
inside the "A bit more" and "More app & XR builds" sections.
"""

import pathlib

import gh

ROOT = pathlib.Path(__file__).resolve().parent.parent
W = 860
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,monospace"
SANS = "'Segoe UI',Inter,Helvetica,Arial,sans-serif"

# ── "A bit more": lead phrase, supporting detail, accent ──
POINTS = [
    ("Computer Engineering Student at KJSSE",
     "Building AI/ML and FinTech systems while maintaining a SGPA of 9.04. "
     "Focus on practical applications that solve real problems.", gh.BLUE),
    ("AI & Machine Learning Engineering",
     "Building ML models for financial markets, anomaly detection, and predictive analytics. "
     "NLP systems for voice assistants and regional language processing.", gh.TEAL),
    ("FinTech Development",
     "Creating practical financial tools — mutual fund analysis platforms, payroll management "
     "systems, and market intelligence dashboards for real-world use.", gh.PURPLE),
    ("Full Stack Development",
     "React and Next.js frontends, Node.js and Flask backends, PostgreSQL and Supabase databases. "
     "Complete end-to-end applications deployed to production.", "#FF7B72"),
    ("Agentic AI & LLM Integration",
     "Implementing LLM-powered agents using OpenAI, Claude, and custom workflows. "
     "Real research agents and intelligent automation systems.", gh.AMBER),
    ("Leadership & Community Building",
     "Founded Finance & Technology Club at KJSSE. Organized FinovateX 2026 — a 7-hour "
     "FinTech dual-event. Contributing to fintech research and discourse.", "#F0A868"),
    ("Industry Experience",
     "Intern at Rayze Technologies (Founders Office), TÜV Rheinland India "
     "(Industrial Services & Cyber Security). Real-world exposure to product and security.", "#A5D6FF"),
    ("Open to Collaboration",
     "Interested in AI/ML projects, FinTech innovation, and building impactful systems. "
     "Available for internships and interesting projects.", gh.TEAL),
]

# ── "More projects": name, what it is, language, chips ──
XR_ROWS = [
    ("FinovateX 2026", "7-hour FinTech dual-event", "Python", ["Event", "Data"]),
    ("Stock Research Agent", "Claude-powered research", "TypeScript", ["React", "Claude API"]),
    ("Pointer Aid 2.0", "SGPI calculator for KJSSE", "JavaScript", ["HTML/CSS/JS"]),
]


def shell(h, uid, body) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}"
     role="img" aria-label="{uid}">
  <defs>
    <linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{gh.BG0}"/><stop offset="100%" stop-color="{gh.BG1}"/>
    </linearGradient>
    <linearGradient id="ac{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6929C4"/><stop offset="50%" stop-color="#1F6FEB"/>
      <stop offset="100%" stop-color="#00D4AA"/>
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


def xr_table() -> str:
    top, row_h = 96, 38
    cols = (26, 292, 604)
    rows = []
    for i, (name, what, lang, chips) in enumerate(XR_ROWS):
        y = top + i * row_h
        colour = gh.lang_colour(lang)
        if i % 2 == 0:
            rows.append(
                f'  <rect x="16" y="{y - 24}" width="{W - 32}" height="{row_h}" rx="7" '
                f'fill="#ffffff" fill-opacity="0.025"/>'
            )
        rows.append(
            f'  <circle cx="{cols[0] + 6}" cy="{y - 5}" r="4.6" fill="{colour}"/>'
            f'<text x="{cols[0] + 20}" y="{y}" '
            f'style="font:600 13.5px {SANS};fill:#ffffff">{gh.esc(name)}</text>'
            f'<text x="{cols[1]}" y="{y}" '
            f'style="font:400 12.5px {SANS};fill:{gh.MUTED}">{gh.esc(what)}</text>'
        )
        x = cols[2]
        for chip in chips:
            cw = len(chip) * 6.6 + 20
            rows.append(
                f'  <rect x="{x:.0f}" y="{y - 15}" width="{cw:.0f}" height="21" rx="10.5" '
                f'fill="{colour}" fill-opacity="0.12" stroke="{colour}" stroke-opacity="0.45"/>'
                f'<text x="{x + cw / 2:.0f}" y="{y - 1}" text-anchor="middle" '
                f'style="font:600 10px {MONO};fill:{colour}">{gh.esc(chip)}</text>'
            )
            x += cw + 7

    height = top + len(XR_ROWS) * row_h + 16
    head = (
        f'  <text x="26" y="38" style="font:700 16px {SANS};fill:{gh.TEAL}">'
        f'◈ More Projects</text>'
        f'<text x="{cols[0]}" y="72" style="font:700 10px {MONO};fill:{gh.DIM};'
        f'letter-spacing:1.5px">PROJECT</text>'
        f'<text x="{cols[1]}" y="72" style="font:700 10px {MONO};fill:{gh.DIM};'
        f'letter-spacing:1.5px">WHAT IT IS</text>'
        f'<text x="{cols[2]}" y="72" style="font:700 10px {MONO};fill:{gh.DIM};'
        f'letter-spacing:1.5px">STACK</text>'
        f'<line x1="22" y1="80" x2="{W - 22}" y2="80" stroke="{gh.LINE}"/>'
    )
    return shell(height, "xr-index", head + "\n" + "\n".join(rows))


def main() -> None:
    out = ROOT / "assets"
    out.mkdir(parents=True, exist_ok=True)
    (out / "about-list.svg").write_text(about_list(), encoding="utf-8")
    (out / "xr-index.svg").write_text(xr_table(), encoding="utf-8")
    print("wrote about-list.svg and xr-index.svg")


if __name__ == "__main__":
    main()
