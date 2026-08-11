#!/usr/bin/env python3
"""Build section header banners with Matrix Hacker Green aesthetic."""

import pathlib

OUT_DIR = pathlib.Path(__file__).resolve().parent.parent / "assets" / "sections"
W, H = 860, 78

# slug, title, kicker, accent, glyph geometry
SECTIONS = [
    (
        "about", "About Me", "WHO I AM AND WHAT I BUILD", "#00FF66",
        '<circle cx="12" cy="8.5" r="4.2" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<path d="M4.2 20.5c0-4.3 3.5-6.6 7.8-6.6s7.8 2.3 7.8 6.6" fill="none" '
        'stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    ),
    (
        "stack", "Tech Stack", "LANGUAGES, FRAMEWORKS, INFRASTRUCTURE", "#00F0FF",
        '<path d="M12 2.6 22 8l-10 5.4L2 8z" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linejoin="round"/>'
        '<path d="M2 13.2 12 18.6l10-5.4" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linejoin="round"/>'
        '<path d="M2 18.2 12 23.6l10-5.4" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linejoin="round" opacity="0.55"/>',
    ),
    (
        "quantum", "Quantum Computing", "SHIPPED, DEPLOYED, PUBLICLY USABLE", "#39FF14",
        '<circle cx="12" cy="12" r="2.6" fill="currentColor"/>'
        '<ellipse cx="12" cy="12" rx="10.4" ry="4.4" fill="none" stroke="currentColor" stroke-width="1.8"/>'
        '<ellipse cx="12" cy="12" rx="10.4" ry="4.4" fill="none" stroke="currentColor" '
        'stroke-width="1.8" transform="rotate(60 12 12)"/>'
        '<ellipse cx="12" cy="12" rx="10.4" ry="4.4" fill="none" stroke="currentColor" '
        'stroke-width="1.8" transform="rotate(120 12 12)"/>',
    ),
    (
        "apps", "App Development · AR / VR", "NATIVE, CROSS-PLATFORM, IMMERSIVE", "#00FF88",
        '<rect x="3" y="2.6" width="11" height="18.8" rx="2.4" fill="none" '
        'stroke="currentColor" stroke-width="2"/>'
        '<line x1="6.6" y1="18.4" x2="10.4" y2="18.4" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round"/>'
        '<path d="M16.4 8.6h3.4a2 2 0 0 1 2 2v3.6a2 2 0 0 1-2 2h-1l-1.4 2-1.4-2h-.6" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
    ),
    (
        "projects", "Featured Projects", "THINGS THAT ACTUALLY RUN", "#FFB800",
        '<rect x="2.6" y="2.6" width="8.2" height="8.2" rx="1.8" fill="none" '
        'stroke="currentColor" stroke-width="2"/>'
        '<rect x="13.2" y="2.6" width="8.2" height="8.2" rx="1.8" fill="currentColor" opacity="0.85"/>'
        '<rect x="2.6" y="13.2" width="8.2" height="8.2" rx="1.8" fill="currentColor" opacity="0.85"/>'
        '<rect x="13.2" y="13.2" width="8.2" height="8.2" rx="1.8" fill="none" '
        'stroke="currentColor" stroke-width="2"/>',
    ),
    (
        "stats", "By the Numbers", "PULLED LIVE FROM THE GITHUB API", "#00F0FF",
        '<line x1="3" y1="21.4" x2="21" y2="21.4" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round"/>'
        '<rect x="4.4" y="13" width="3.8" height="6" rx="1.2" fill="currentColor"/>'
        '<rect x="10.1" y="8" width="3.8" height="11" rx="1.2" fill="currentColor"/>'
        '<rect x="15.8" y="3.4" width="3.8" height="15.6" rx="1.2" fill="currentColor"/>',
    ),
    (
        "snake", "Contribution Snake", "WATCH IT EAT A YEAR OF COMMITS", "#00FF66",
        '<rect x="2.4" y="9.6" width="4.6" height="4.6" rx="1.2" fill="currentColor" opacity="0.4"/>'
        '<rect x="8.2" y="9.6" width="4.6" height="4.6" rx="1.2" fill="currentColor" opacity="0.7"/>'
        '<rect x="14" y="9.6" width="4.6" height="4.6" rx="1.2" fill="currentColor"/>'
        '<circle cx="21.2" cy="11.9" r="1.5" fill="currentColor"/>',
    ),
    (
        "connect", "Connect", "OPEN TO COLLABORATION", "#39FF14",
        '<circle cx="6.4" cy="12" r="3.6" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<circle cx="17.6" cy="6.6" r="3.2" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<circle cx="17.6" cy="17.4" r="3.2" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<line x1="9.6" y1="10.4" x2="14.6" y2="7.9" stroke="currentColor" stroke-width="2"/>'
        '<line x1="9.6" y1="13.6" x2="14.6" y2="16.1" stroke="currentColor" stroke-width="2"/>',
    ),
]


def build(slug: str, title: str, kicker: str, accent: str, glyph: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"
     role="img" aria-label="{title}">
  <title>{title}</title>
  <defs>
    <linearGradient id="bg-{slug}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="{accent}" stop-opacity="0.2"/>
      <stop offset="55%"  stop-color="#050a07" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#050a07" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="rule-{slug}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="{accent}"/>
      <stop offset="60%"  stop-color="{accent}" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="badge-{slug}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%"   stop-color="{accent}" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0.08"/>
    </linearGradient>
    <filter id="soft-{slug}" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="3.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style>
      .t-{slug} {{ font-family:"Segoe UI",Inter,Helvetica,Arial,sans-serif;
                   font-size:27px; font-weight:800; fill:#ffffff; letter-spacing:-0.2px; }}
      .k-{slug} {{ font-family:"JetBrains Mono","SFMono-Regular",Consolas,monospace;
                   font-size:11px; font-weight:600; fill:{accent};
                   fill-opacity:0.85; letter-spacing:2px; }}
    </style>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bg-{slug})"/>

  <!-- Accent Rule -->
  <rect x="0" y="74" width="{W}" height="2" fill="url(#rule-{slug})"/>

  <!-- Glyph Box -->
  <rect x="18" y="16" width="44" height="44" rx="10" fill="url(#badge-{slug})"
        stroke="{accent}" stroke-opacity="0.5" stroke-width="1.2"/>
  <g transform="translate(28 26)" color="{accent}" filter="url(#soft-{slug})">
    {glyph}
  </g>

  <!-- Titles -->
  <text x="76" y="38" class="k-{slug}">{kicker}</text>
  <text x="76" y="62" class="t-{slug}">{title}</text>
</svg>
'''


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for slug, title, kicker, accent, glyph in SECTIONS:
        path = OUT_DIR / f"{slug}.svg"
        path.write_text(build(slug, title, kicker, accent, glyph), encoding="utf-8")
        print(f"wrote {path.name}")


if __name__ == "__main__":
    main()
