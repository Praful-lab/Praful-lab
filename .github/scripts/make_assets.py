"""Generate the animated SVG artwork used in the profile README.

Run from the repo root:  python .github/scripts/make_assets.py
Writes assets/hero.svg, assets/boot.svg, assets/divider.svg and assets/card-*.svg.
"""
import os
import random
from html import escape

random.seed(17)
os.makedirs("assets", exist_ok=True)

SANS = "'Segoe UI', 'Helvetica Neue', Ubuntu, Arial, sans-serif"
MONO = "'JetBrains Mono', 'Cascadia Code', Consolas, 'Liberation Mono', Menlo, monospace"
BG, CYAN, VIOLET, PINK, GREEN, DIM, TEXT = "#070b14", "#22d3ee", "#8b5cf6", "#ec4899", "#34d399", "#64748b", "#e2e8f0"


def save(name, svg):
    with open(os.path.join("assets", name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote assets/" + name)


# ─────────────────────────────── HERO ───────────────────────────────
def hero():
    W, H = 1200, 460
    layers_x = [815, 920, 1025, 1130]
    counts = [4, 6, 6, 3]
    nodes = []
    for x, n in zip(layers_x, counts):
        span = 250
        top = 105 + (span - (n - 1) * 50) / 2 if n > 1 else 230
        nodes.append([(x, top + i * 50) for i in range(n)])

    edges = []
    for a, b in zip(nodes, nodes[1:]):
        for p in a:
            for q in b:
                edges.append(f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}"/>')

    pulses = []
    for k in range(16):
        path = [random.choice(layer) for layer in nodes]
        d = "M" + " L".join(f"{x},{y}" for x, y in path)
        colour = random.choice([CYAN, CYAN, VIOLET, PINK])
        begin = round(k * 0.35, 2)
        pulses.append(
            f'<circle r="3.2" fill="{colour}" filter="url(#glow)" opacity="0">'
            f'<animateMotion dur="2.6s" begin="{begin}s" repeatCount="indefinite" path="{d}"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.85;1" dur="2.6s" begin="{begin}s" repeatCount="indefinite"/>'
            f'</circle>')

    node_svg = []
    for li, layer in enumerate(nodes):
        for ni, (x, y) in enumerate(layer):
            d = round(random.uniform(0, 2.5), 2)
            node_svg.append(
                f'<circle cx="{x}" cy="{y}" r="13" fill="{CYAN}" opacity="0.12">'
                f'<animate attributeName="r" values="9;16;9" dur="2.4s" begin="{d}s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0.05;0.28;0.05" dur="2.4s" begin="{d}s" repeatCount="indefinite"/></circle>'
                f'<circle cx="{x}" cy="{y}" r="6.5" fill="{BG}" stroke="{CYAN if li % 2 == 0 else VIOLET}" stroke-width="2.2"/>')

    labels = [("INPUT", layers_x[0]), ("ATTENTION", layers_x[1] + 52), ("OUTPUT", layers_x[3])]
    layer_labels = "".join(
        f'<text x="{x}" y="395" text-anchor="middle" class="m" font-size="11" fill="{DIM}" letter-spacing="3">{t}</text>'
        for t, x in labels)

    particles = []
    for _ in range(34):
        x = random.randint(20, W - 20)
        y = random.randint(40, H)
        d = round(random.uniform(5, 11), 1)
        b = round(random.uniform(0, 8), 1)
        r = random.choice([0.8, 1.1, 1.5])
        particles.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{random.choice([CYAN, VIOLET, TEXT])}">'
            f'<animate attributeName="cy" values="{y};{y - 120}" dur="{d}s" begin="{b}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.8;0" dur="{d}s" begin="{b}s" repeatCount="indefinite"/></circle>')

    chips, cx = [], 74
    for label, colour in [("ONLINE", GREEN), ("AI Product Developer · EduFlourish", CYAN),
                          ("Founder · BotifyIndia", VIOLET), ("Mangalore, IN", DIM)]:
        w = len(label) * 7.6 + (44 if label == "ONLINE" else 28)
        dot = (f'<circle cx="{cx + 16}" cy="352" r="4" fill="{GREEN}"><animate attributeName="opacity" values="1;0.2;1" dur="1.4s" repeatCount="indefinite"/></circle>'
               if label == "ONLINE" else "")
        tx = cx + (30 if label == "ONLINE" else 14)
        chips.append(
            f'<rect x="{cx}" y="337" width="{w:.0f}" height="30" rx="15" fill="{colour}" fill-opacity="0.08" stroke="{colour}" stroke-opacity="0.55"/>'
            f'{dot}<text x="{tx}" y="357" class="m" font-size="12.5" fill="{TEXT}">{escape(label)}</text>')
        cx += w + 10

    brackets = "".join(
        f'<path d="{d}" fill="none" stroke="{CYAN}" stroke-width="2" opacity="0.7"/>'
        for d in ["M18,48 V18 H48", f"M{W - 48},18 H{W - 18} V48",
                  f"M18,{H - 48} V{H - 18} H48", f"M{W - 48},{H - 18} H{W - 18} V{H - 48}"])

    sub = "LLMs · AI agents · automation that ships"
    sub_w = len(sub) * 11.6

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <radialGradient id="bg" cx="70%" cy="40%" r="80%">
    <stop offset="0%" stop-color="#1e1145"/><stop offset="45%" stop-color="#0b1023"/><stop offset="100%" stop-color="{BG}"/>
  </radialGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="#334155" stroke-width="0.6"/>
  </pattern>
  <radialGradient id="fade" cx="50%" cy="50%" r="60%">
    <stop offset="0%" stop-color="#fff" stop-opacity="0.55"/><stop offset="100%" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <mask id="gm"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
  <linearGradient id="name" x1="0" y1="0" x2="700" y2="0" gradientUnits="userSpaceOnUse" spreadMethod="reflect">
    <stop offset="0%" stop-color="{CYAN}"/><stop offset="50%" stop-color="#ffffff"/><stop offset="100%" stop-color="{VIOLET}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="0 0;700 0;0 0" dur="7s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{CYAN}" stop-opacity="0"/><stop offset="100%" stop-color="{CYAN}" stop-opacity="0.35"/>
  </linearGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="bigglow" x="-20%" y="-50%" width="140%" height="200%">
    <feGaussianBlur stdDeviation="14"/>
  </filter>
  <clipPath id="type"><rect x="72" y="262" height="34" width="0">
    <animate attributeName="width" values="0;{sub_w:.0f};{sub_w:.0f};0" keyTimes="0;0.35;0.9;1" dur="9s" repeatCount="indefinite"/>
  </rect></clipPath>
  <style>
    .s{{font-family:{SANS}}} .m{{font-family:{MONO}}}
  </style>
</defs>

<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
<rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gm)"/>
<g>{''.join(particles)}</g>

<!-- neural network -->
<g stroke="{VIOLET}" stroke-opacity="0.18" stroke-width="1">{''.join(edges)}</g>
<g>{''.join(pulses)}</g>
<g>{''.join(node_svg)}</g>
{layer_labels}

<!-- identity -->
<text x="74" y="128" class="m" font-size="14" fill="{CYAN}" letter-spacing="4">// AI PRODUCT DEVELOPER</text>
<text x="72" y="222" class="s" font-size="96" font-weight="800" fill="{VIOLET}" opacity="0.55" filter="url(#bigglow)">PRAFUL U S</text>
<g>
  <text x="76" y="219" class="s" font-size="96" font-weight="800" fill="{PINK}" opacity="0">PRAFUL U S
    <animate attributeName="opacity" values="0;0;0.75;0;0.6;0" keyTimes="0;0.86;0.88;0.9;0.93;1" dur="6s" repeatCount="indefinite"/></text>
  <text x="68" y="225" class="s" font-size="96" font-weight="800" fill="{CYAN}" opacity="0">PRAFUL U S
    <animate attributeName="opacity" values="0;0;0.75;0;0.6;0" keyTimes="0;0.86;0.885;0.905;0.935;1" dur="6s" repeatCount="indefinite"/></text>
  <text x="72" y="222" class="s" font-size="96" font-weight="800" fill="url(#name)">PRAFUL U S</text>
</g>

<g clip-path="url(#type)">
  <text x="74" y="286" class="m" font-size="20" fill="{TEXT}">{escape(sub)}</text>
</g>
<rect x="74" y="266" width="11" height="24" fill="{CYAN}">
  <animate attributeName="x" values="76;{76 + sub_w:.0f};{76 + sub_w:.0f};76" keyTimes="0;0.35;0.9;1" dur="9s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite"/>
</rect>

{''.join(chips)}

<!-- HUD -->
{brackets}
<text x="{W - 40}" y="46" text-anchor="end" class="m" font-size="11" fill="{DIM}" letter-spacing="2">SYS.v2026 · NEURAL CORE ACTIVE</text>
<rect x="0" y="-60" width="{W}" height="60" fill="url(#scan)" opacity="0.6">
  <animate attributeName="y" values="-60;{H}" dur="5.5s" repeatCount="indefinite"/>
</rect>
</svg>'''
    save("hero.svg", svg)


# ─────────────────────────────── BOOT TERMINAL ───────────────────────────────
def boot():
    W = 1000
    lines = [
        ("cmd", "$ ./praful --boot --mode=builder"),
        ("ok", "loading weights ........ qwen3-4b + lora[tulu]"),
        ("ok", "spawning agents ........ hiring · whatsapp · call-trainer"),
        ("ok", "linking tools .......... n8n · waha · meritto · google calendar"),
        ("ok", "deploying .............. ai hiring pipeline → round 3 live"),
        ("run", "researching ............ android RAT detection (m.tech)"),
        ("out", "> status: ONLINE — ready to build with you"),
    ]
    LH, TOP = 38, 92
    H = TOP + len(lines) * LH + 8
    cycle, step = 14.0, 0.9
    rows = []
    for i, (kind, text) in enumerate(lines):
        y = TOP + i * LH
        t0 = 0.6 + i * step
        k0, k1 = t0 / cycle, (t0 + 0.25) / cycle
        anim = (f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{k0:.3f};{k1:.3f};0.93;1" '
                f'dur="{cycle}s" repeatCount="indefinite"/>')
        if kind == "cmd":
            body = f'<text x="40" y="{y}" class="m" font-size="17" fill="{TEXT}">{escape(text)}</text>'
        elif kind == "out":
            body = f'<text x="40" y="{y}" class="m" font-size="17" font-weight="700" fill="{GREEN}">{escape(text)}</text>'
        else:
            tag, colour = ("[ ok ]", GREEN) if kind == "ok" else ("[ ⟳  ]", "#fbbf24")
            body = (f'<text x="40" y="{y}" class="m" font-size="17" fill="{colour}">{tag}</text>'
                    f'<text x="120" y="{y}" class="m" font-size="17" fill="#cbd5e1">{escape(text)}</text>')
            if kind == "run":
                bx = 700
                body += (f'<rect x="{bx}" y="{y - 13}" width="240" height="14" rx="3" fill="#1e293b"/>'
                         f'<rect x="{bx}" y="{y - 13}" width="70" height="14" rx="3" fill="url(#bar)">'
                         f'<animate attributeName="x" values="{bx};{bx + 170};{bx}" dur="2.4s" repeatCount="indefinite"/></rect>')
        rows.append(f'<g opacity="0">{anim}{body}</g>')

    cur_y = TOP + (len(lines) - 1) * LH
    tail = len("> status: ONLINE — ready to build with you") * 10.25 + 46
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="frame" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{CYAN}"/><stop offset="50%" stop-color="{VIOLET}"/><stop offset="100%" stop-color="{PINK}"/>
  </linearGradient>
  <linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{VIOLET}"/><stop offset="100%" stop-color="{CYAN}"/>
  </linearGradient>
  <style>.m{{font-family:{MONO}}}</style>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="#0b1020" stroke="url(#frame)" stroke-width="2"/>
<rect x="1" y="1" width="{W - 2}" height="44" rx="14" fill="#111827"/>
<rect x="1" y="30" width="{W - 2}" height="15" fill="#111827"/>
<circle cx="28" cy="23" r="7" fill="#ff5f57"/><circle cx="52" cy="23" r="7" fill="#febc2e"/><circle cx="76" cy="23" r="7" fill="#28c840"/>
<text x="{W / 2}" y="28" text-anchor="middle" class="m" font-size="13" fill="{DIM}">praful@ai-lab: ~/profile</text>
{''.join(rows)}
<rect x="{tail:.0f}" y="{cur_y - 15}" width="10" height="20" fill="{GREEN}" opacity="0">
  <animate attributeName="opacity" values="0;0;1;0;1;0;1;0" keyTimes="0;{(0.6 + 6 * step) / cycle:.3f};0.6;0.66;0.72;0.8;0.88;1" dur="{cycle}s" repeatCount="indefinite"/>
</rect>
</svg>'''
    save("boot.svg", svg)


# ─────────────────────────────── DIVIDER ───────────────────────────────
def divider():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="14" viewBox="0 0 1200 14">
<defs>
  <linearGradient id="base" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{VIOLET}" stop-opacity="0"/><stop offset="50%" stop-color="{VIOLET}" stop-opacity="0.6"/><stop offset="100%" stop-color="{VIOLET}" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="spark"><stop offset="0%" stop-color="#fff"/><stop offset="35%" stop-color="{CYAN}"/><stop offset="100%" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
</defs>
<rect y="6" width="1200" height="2" fill="url(#base)"/>
<ellipse cy="7" rx="90" ry="6" fill="url(#spark)">
  <animate attributeName="cx" values="-100;1300" dur="3.2s" repeatCount="indefinite"/>
</ellipse>
</svg>'''
    save("divider.svg", svg)


# ─────────────────────────────── PROJECT CARDS ───────────────────────────────
def card(slug, kicker, title, lines, chips, accent, glyph):
    W, H = 580, 260
    peri = 2 * (W - 4 + H - 4)
    chip_svg, cx = [], 28
    for c in chips:
        w = len(c) * 7.4 + 22
        chip_svg.append(f'<rect x="{cx}" y="206" width="{w:.0f}" height="26" rx="13" fill="{accent}" fill-opacity="0.1" stroke="{accent}" stroke-opacity="0.5"/>'
                        f'<text x="{cx + 11}" y="223.5" class="m" font-size="12" fill="{TEXT}">{escape(c)}</text>')
        cx += w + 8
    body = "".join(f'<text x="28" y="{128 + i * 25}" class="s" font-size="15.5" fill="#cbd5e1">{escape(t)}</text>'
                   for i, t in enumerate(lines))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#111733"/><stop offset="100%" stop-color="{BG}"/>
  </linearGradient>
  <linearGradient id="run" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{accent}" stop-opacity="0"/><stop offset="100%" stop-color="{accent}"/>
  </linearGradient>
  <radialGradient id="orb" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="{accent}" stop-opacity="0.45"/><stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
  </radialGradient>
  <filter id="glow" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="2.5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <style>.s{{font-family:{SANS}}} .m{{font-family:{MONO}}}</style>
</defs>
<rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="16" fill="url(#bg)" stroke="#1e293b" stroke-width="1.5"/>
<circle cx="{W - 70}" cy="70" r="110" fill="url(#orb)">
  <animate attributeName="r" values="95;125;95" dur="5s" repeatCount="indefinite"/>
</circle>
<rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="16" fill="none" stroke="{accent}" stroke-width="2.5"
      stroke-dasharray="160 {peri - 160:.0f}" filter="url(#glow)">
  <animate attributeName="stroke-dashoffset" values="0;-{peri:.0f}" dur="6s" repeatCount="indefinite"/>
</rect>
<text x="{W - 70}" y="92" text-anchor="middle" class="s" font-size="60" fill="{accent}" opacity="0.9">{glyph}</text>
<text x="28" y="48" class="m" font-size="12" fill="{accent}" letter-spacing="3">{escape(kicker)}</text>
<text x="28" y="88" class="s" font-size="30" font-weight="800" fill="#ffffff">{escape(title)}</text>
{body}
{''.join(chip_svg)}
</svg>'''
    save(f"card-{slug}.svg", svg)


if __name__ == "__main__":
    hero()
    boot()
    divider()
    card("voxintel", "LOW-RESOURCE LLM", "VoxIntel",
         ["Tulu had almost no NLP tooling. I fine-tuned", "Qwen3-4B with LoRA on Kaggle and shipped chat,", "translate, learn and voice — plus a 19-page audit."],
         ["Qwen3-4B", "LoRA", "FastAPI", "React 19"], CYAN, "◈")
    card("hiring", "AI AGENT · IN PRODUCTION", "AI Hiring Pipeline",
         ["Résumé → LLM-drafted test → AI voice interview", "→ live proctoring → auto-booked Google Meet.", "One HR portal: the AI screens, HR decides."],
         ["LLM", "Voice AI", "Proctoring", "Calendar API"], VIOLET, "⬡")
    card("learnloop", "CONVERSATIONAL AI", "LearnLoop",
         ["An LLM plays the parent on the other end of", "the line, so new staff rehearse product calls", "safely before they ever talk to a real lead."],
         ["LLM role-play", "Web app", "Render"], PINK, "◉")
    card("botify", "FOUNDER · WHATSAPP AGENTS", "BotifyIndia",
         ["WhatsApp AI agents that answer customers,", "qualify leads and follow up — 24/7 — for", "small businesses, on reusable infrastructure."],
         ["n8n", "WAHA", "LLM routing", "CRM"], GREEN, "◆")
