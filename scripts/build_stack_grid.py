#!/usr/bin/env python3
"""Render the tech-stack section as real logo tiles with a label under each,
grouped by category.

skillicons.dev serves single icons too, not just the multi-icon strip — so
each tile embeds that icon's actual URL and adds a caption beneath it,
giving real logos *and* names instead of choosing between the two.
"""

import pathlib

import gh

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "stack-grid.svg"
W = 860
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,monospace"
SANS = "'Segoe UI',Inter,Helvetica,Arial,sans-serif"
ICON = "https://skillicons.dev/icons?i={slug}&amp;theme=dark"

# category label, accent colour, [(display label, skillicons slug), ...]
CATEGORIES = [
    ("Languages", "#00FF66", [
        ("Python", "python"), ("TypeScript", "ts"), ("JavaScript", "js"),
        ("C++", "cpp"), ("C", "c"), ("Java", "java"),
    ]),
    ("Frontend Frameworks & UI", "#00F0FF", [
        ("React", "react"), ("Next.js", "nextjs"), ("Vite", "vite"),
        ("HTML5", "html"), ("CSS5", "css"), ("Tailwind", "tailwind"),
        ("Electron", "electron"), ("Figma", "figma"),
    ]),
    ("Backend & APIs", "#39FF14", [
        ("Node.js", "nodejs"), ("Express", "express"), ("Flask", "flask"),
        ("FastAPI", "fastapi"), ("Python", "python"),
    ]),
    ("AI / ML · Data Science", "#00F0FF", [
        ("PyTorch", "pytorch"), ("TensorFlow", "tensorflow"), ("scikit-learn", "sklearn"),
        ("Anaconda", "anaconda"), ("D3.js", "d3"),
    ]),
    ("Databases & Cloud", "#FFB800", [
        ("PostgreSQL", "postgres"), ("Supabase", "supabase"), ("MongoDB", "mongodb"),
        ("MySQL", "mysql"), ("Vercel", "vercel"), ("Netlify", "netlify"),
    ]),
    ("Developer Tools & Environment", "#A78BFA", [
        ("Git", "git"), ("GitHub", "github"), ("VS Code", "vscode"),
        ("Linux", "linux"), ("Docker", "docker"), ("Windows", "windows"),
        ("Postman", "postman"),
    ]),
]

TILE_W, TILE_H = 84, 78
ICON_SIZE = 38
CAT_GAP = 26
PAD_X = 26


def wrap_tiles(skills, top_y):
    """Flow tiles left-to-right, wrapping to a new row at the card width."""
    rows, x, y = [], PAD_X, top_y
    row = []
    for label, slug in skills:
        if x + TILE_W > W - PAD_X and row:
            rows.append((y, row))
            row, x = [], PAD_X
            y += TILE_H
        row.append((x, label, slug))
        x += TILE_W
    if row:
        rows.append((y, row))
    return rows, y + TILE_H


def build() -> str:
    body = []
    y = 58
    for cat_label, accent, skills in CATEGORIES:
        body.append(
            f'  <text x="{PAD_X}" y="{y}" style="font:700 12.5px {MONO};fill:{accent};'
            f'letter-spacing:1.4px">{gh.esc(cat_label.upper())}</text>'
        )
        rows, y_after = wrap_tiles(skills, y + 22)
        for row_y, tiles in rows:
            for x, label, slug in tiles:
                cx = x + TILE_W / 2
                body.append(
                    f'  <image href="{ICON.format(slug=slug)}" x="{cx - ICON_SIZE / 2:.0f}" '
                    f'y="{row_y:.0f}" width="{ICON_SIZE}" height="{ICON_SIZE}"/>'
                    f'<text x="{cx:.0f}" y="{row_y + ICON_SIZE + 16:.0f}" text-anchor="middle" '
                    f'style="font:600 10px {SANS};fill:{gh.MUTED}">{gh.esc(label)}</text>'
                )
        y = y_after + CAT_GAP

    height = y - CAT_GAP + 18
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {W} {height:.0f}" width="{W}" height="{height:.0f}" role="img"
     aria-label="Core technologies, grouped by category">
  <title>Core technologies</title>
  <defs>
    <linearGradient id="sbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{gh.BG0}"/><stop offset="100%" stop-color="{gh.BG1}"/>
    </linearGradient>
    <linearGradient id="sac" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00FF66"/><stop offset="50%" stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#39FF14"/>
    </linearGradient>
  </defs>

  <rect width="{W}" height="{height:.0f}" rx="13" fill="url(#sbg)"/>
  <rect x="1" y="1" width="{W - 2}" height="{height - 2:.0f}" rx="12" fill="none"
        stroke="url(#sac)" stroke-opacity="0.4" stroke-width="2"/>

{chr(10).join(body)}
</svg>
'''


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
