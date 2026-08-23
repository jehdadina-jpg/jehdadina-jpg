#!/usr/bin/env python3
"""Render the "about me" snippet as a terminal window instead of a plain code fence.

GitHub's own syntax highlighting is fine but visually flat, and it cannot show
window chrome, line numbers, or a blinking cursor. Drawing it ourselves gives
the section a real editor look that matches the other cards.
"""

import pathlib

import gh

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "about-code.svg"

KW, VAR, STR, NUM, PUN, CMT, PROP = (
    "#00FF66", "#00F0FF", "#A3FFC2", "#FFB800", "#52996A", "#2B5E39", "#39FF14",
)

# (indent, [(text, colour), ...]) — tokenised by hand so the colours are exact.
LINES = [
    [("const", KW), (" jeh", VAR), (" = ", PUN), ("{", PUN)],
    [("  name", PROP), (": ", PUN), ('"Jeh Dadina"', STR), (",", PUN)],
    [("  role", PROP), (": ", PUN), ('"Computer Engineering Student"', STR), (",", PUN)],
    [("  institution", PROP), (": ", PUN), ('"KJ Somaiya School of Engineering"', STR), (",", PUN)],
    [("  location", PROP), (": ", PUN), ('"Mumbai, India"', STR), (",", PUN)],
    [("  focus", PROP), (": ", PUN), ("[", PUN), ('"AI/ML"', STR), (", ", PUN),
     ('"FinTech"', STR), (", ", PUN), ('"Full Stack"', STR), ("],", PUN)],
    [("  building", PROP), (": ", PUN), ("[", PUN), ('"MFScope"', STR), (", ", PUN),
     ('"Anomaly Terminal"', STR), (", ", PUN), ('"SwipeRight"', STR), (", ", PUN),
     ('"GitControl"', STR), ("],", PUN)],
    [("  stack", PROP), (": ", PUN), ("[", PUN), ('"Python"', STR), (", ", PUN),
     ('"TypeScript"', STR), (", ", PUN), ('"React"', STR), (", ", PUN),
     ('"Node.js"', STR), (", ", PUN), ('"ML"', STR), ("],", PUN)],
    [("  currentSGPA", PROP), (": ", PUN), ("9.04", NUM), (",", PUN)],
    [("}", PUN), (" as", KW), (" const", KW), (";", PUN)],
]

CHAR_W = 7.22  # advance width of the mono stack at 12px
FONT = 12
TOP = 62
LEADING = 19.5
W = 860
H = TOP + len(LINES) * LEADING + 26


def build() -> str:
    rows = []
    for i, tokens in enumerate(LINES):
        y = TOP + i * LEADING
        col = 0
        spans = []
        for text, colour in tokens:
            spans.append(
                f'<tspan x="{62 + col * CHAR_W:.1f}" fill="{colour}">{gh.esc(text)}</tspan>'
            )
            col += len(text)
        rows.append(
            f'    <text y="{y:.1f}" class="ln">'
            f'<tspan x="30" fill="#2B5E39">{i + 1:>2}</tspan>{"".join(spans)}</text>'
        )

    last_line_len = sum(len(text) for text, _ in LINES[-1])
    cursor_x = 62 + last_line_len * CHAR_W + CHAR_W
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H:.0f}"
     role="img" aria-label="About Jeh, as a TypeScript object">
  <title>const jeh = {{ ... }}</title>
  <defs>
    <linearGradient id="cbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{gh.BG0}"/><stop offset="100%" stop-color="{gh.BG1}"/>
    </linearGradient>
    <linearGradient id="cac" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00FF66"/><stop offset="50%" stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#39FF14"/>
    </linearGradient>
    <style>
      .ln  {{ font-family:"JetBrains Mono","SFMono-Regular",Consolas,monospace;
              font-size:{FONT}px; }}
      .tab {{ font-family:"JetBrains Mono",Consolas,monospace; font-size:11.5px;
              fill:{gh.MUTED}; }}
    </style>
  </defs>

  <rect width="{W}" height="{H:.0f}" rx="12" fill="url(#cbg)"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2:.0f}" rx="11" fill="none"
        stroke="url(#cac)" stroke-opacity="0.4" stroke-width="2"/>

  <!-- window chrome -->
  <path d="M1 13a12 12 0 0 1 12-12h834a12 12 0 0 1 12 12v25H1z" fill="#0b0e14" fill-opacity="0.8"/>
  <line x1="1" y1="38" x2="859" y2="38" stroke="{gh.LINE}"/>
  <circle cx="24" cy="20" r="5.5" fill="#FF5F57"/>
  <circle cx="43" cy="20" r="5.5" fill="#FEBC2E"/>
  <circle cx="62" cy="20" r="5.5" fill="#28C840"/>
  <text x="86" y="24" class="tab">jeh.ts</text>
  <text x="838" y="24" class="tab" text-anchor="end">TypeScript</text>

{chr(10).join(rows)}

  <rect x="{cursor_x:.1f}" y="{TOP + (len(LINES) - 1) * LEADING - 10:.1f}" width="8" height="14" fill="{gh.TEAL}">
    <animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/>
  </rect>
</svg>
'''


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
