"""Render a 30-day contribution activity graph as an SVG, using the GitHub GraphQL API.

Usage: python activity_graph.py <username> <output.svg>
Needs GITHUB_TOKEN in the environment.
"""
import datetime as dt
import json
import os
import sys
import urllib.request

USER, OUT = sys.argv[1], sys.argv[2]
DAYS = 30

query = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}"""

req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": query, "variables": {"login": USER}}).encode(),
    headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}",
             "Content-Type": "application/json"},
)
with urllib.request.urlopen(req) as r:
    data = json.load(r)

days = [d for w in data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
        for d in w["contributionDays"]]
days = days[-DAYS:]
counts = [d["contributionCount"] for d in days]
total = sum(counts)

W, H = 900, 300
L, R, T, B = 50, 25, 60, 45
pw, ph = W - L - R, H - T - B
top = max(max(counts), 4)
step = pw / (len(counts) - 1)

def xy(i, c):
    return L + i * step, T + ph - (c / top) * ph

pts = [xy(i, c) for i, c in enumerate(counts)]
line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
area = f"{L},{T + ph} " + line + f" {L + pw},{T + ph}"

grid, labels = [], []
for k in range(5):
    v = round(top * k / 4)
    y = T + ph - (v / top) * ph
    grid.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L + pw}" y2="{y:.1f}" class="g"/>')
    labels.append(f'<text x="{L - 10}" y="{y + 4:.1f}" class="t" text-anchor="end">{v}</text>')
for i, d in enumerate(days):
    if i % 5 == 0 or i == len(days) - 1:
        x, _ = xy(i, 0)
        lab = dt.date.fromisoformat(d["date"]).strftime("%d %b")
        labels.append(f'<text x="{x:.1f}" y="{T + ph + 22}" class="t" text-anchor="middle">{lab}</text>')

dots = "".join(
    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" class="d"><title>{days[i]["date"]}: {counts[i]}</title></circle>'
    for i, (x, y) in enumerate(pts))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="a" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.55"/>
    <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="l" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#8b5cf6"/><stop offset="100%" stop-color="#22d3ee"/>
  </linearGradient>
  <style>
    .g{{stroke:#21262d;stroke-width:1}}
    .t{{fill:#8b949e;font:12px 'Segoe UI',Ubuntu,sans-serif}}
    .h{{fill:#22d3ee;font:600 18px 'Segoe UI',Ubuntu,sans-serif}}
    .s{{fill:#c9d1d9;font:13px 'Segoe UI',Ubuntu,sans-serif}}
    .d{{fill:#ffffff;stroke:#22d3ee;stroke-width:2}}
  </style>
</defs>
<rect width="{W}" height="{H}" rx="12" fill="#0d1117"/>
<text x="{L}" y="32" class="h">Contribution activity · last {DAYS} days</text>
<text x="{W - R}" y="32" class="s" text-anchor="end">{total} contributions</text>
{''.join(grid)}
<polygon points="{area}" fill="url(#a)"/>
<polyline points="{line}" fill="none" stroke="url(#l)" stroke-width="3" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0">
  <animate attributeName="stroke-dashoffset" from="1" to="0" dur="2.2s" fill="freeze"/>
</polyline>
{dots}
{''.join(labels)}
</svg>'''

os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT}: {total} contributions over {DAYS} days")
