#!/usr/bin/env python3
"""
generate_tkonti.py — Generates IFRS 9 T-konti HTML from JSON input.

Usage:
    python scripts/generate_tkonti.py input.json output.html

Input JSON schema:
{
  "title": "IFRS 9 Kursregulering — Matched Funding",
  "subtitle": "Udlån (FVTPL) + obligation (FVTPL). Samme serie.",
  "principles": [
    "Udlån bogføres til FV (mid). Kursskæring = realiseret day-one (B5.1.2A).",
    "Obligationer udstedt til mid → ingen kursskæring på passiv."
  ],
  "scenario": "Dag 1: <tag-a>A</tag-a> Udlån nom. 1M, udbetalt kurs 98,9, mid 99,4.",
  "loan_tags": {"A": "a", "B": "b"},
  "days": [
    {
      "title": "Dag 1 — A Udlån + obligation, mid 99,4",
      "callouts": [
        {"color": "green", "html": "<strong>Udlån:</strong> Dr Udlån 994.000 / Cr Kasse 989.000 / Cr Realiseret 5.000"}
      ],
      "netting": [
        {"color": "red", "html": "Tab udlån: <strong>−5.000</strong>"},
        {"color": "green", "html": "Gevinst obl: <strong>+5.000</strong>"},
        {"color": "grey", "html": "<strong>Netto: 0</strong>"}
      ],
      "accounts": [
        {
          "title": "Udlån (FVTPL aktiv)",
          "rows": [
            {"debet": "Oprettelse 994.000", "kredit": ""},
            {"debet": "", "kredit": "", "total": true, "debet_total": "Saldo: 994.000", "kredit_total": ""}
          ]
        },
        {
          "title": "Kasse",
          "rows": [
            {"debet": "", "kredit": "Udbetaling 989.000"},
            {"debet": "Obl.provenu 994.000", "kredit": ""},
            {"debet": "", "kredit": "", "total": true, "debet_total": "Saldo: 5.000", "kredit_total": ""}
          ]
        }
      ],
      "saldi": [
        {"label": "Udlån", "value": "994.000"},
        {"label": "Obl", "value": "994.000"},
        {"label": "Kasse", "value": "5.000", "css": "saldo-pos"},
        {"label": "Ureal", "value": "0", "css": "saldo-zero"},
        {"label": "Real", "value": "+5.000", "css": "saldo-pos"},
        {"label": "P&L", "value": "+5.000", "css": "saldo-pos"},
        {"label": "Bal", "value": "✓", "css": "saldo-zero"}
      ]
    }
  ],
  "summary_cards": [
    {"label": "Kursskæring A", "value": "+5.000", "sub": "FV 994k − udbetalt 989k", "color": "teal"},
    {"label": "Total P&L", "value": "+5.000", "sub": "= Kasse = kursskæring", "color": "amber"}
  ],
  "netting_table": {
    "headers": ["Effekt", "Udlån", "Obl", "Netto"],
    "sections": [
      {
        "title": "Kursregulering (urealiseret)",
        "rows": [["Dag 2: 99,4→97,25", "−21.500", "+21.500", "0"]]
      }
    ],
    "total": ["Total P&L", "", "", "+5.000"]
  },
  "conclusion": "I et matched-funded realkreditinstitut er den eneste permanente P&L kursskæringen."
}

Notes on the JSON:
- In "scenario" and callout html, use <tag-a>X</tag-a> or <tag-b>X</tag-b> for loan tags.
- In account rows, use <delta>text</delta> for green and <delta-neg>text</delta-neg> for red.
- The "css" field in saldi items is optional; defaults to "" (neutral).
- "netting" array in a day is optional.
- "netting_table" and "summary_cards" at top level are optional.
"""

import json
import sys
import html as html_module

CSS = r"""
:root {
  --font-sans: system-ui, -apple-system, sans-serif;
  --color-text-primary: #1a1a1a;
  --color-text-secondary: #666;
  --color-text-tertiary: #999;
  --color-background-secondary: #f5f5f3;
  --color-border-tertiary: rgba(0,0,0,0.12);
  --color-border-secondary: rgba(0,0,0,0.2);
  --border-radius-lg: 12px;
}
@media (prefers-color-scheme: dark) {
  :root {
    --color-text-primary: #e0dfd8;
    --color-text-secondary: #9c9a92;
    --color-text-tertiary: #73726c;
    --color-background-secondary: #2a2a28;
    --color-border-tertiary: rgba(255,255,255,0.12);
    --color-border-secondary: rgba(255,255,255,0.2);
  }
  body { background: #1a1a18; }
}
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: var(--font-sans); color: var(--color-text-primary); padding: 24px; max-width: 1300px; margin: 0 auto; }
h1 { font-size: 20px; font-weight: 600; margin-bottom: 4px; }
.subtitle { font-size: 13px; color: var(--color-text-secondary); margin-bottom: 20px; }
.day { margin-bottom: 24px; }
.day-title { font-size: 16px; font-weight: 500; margin-bottom: 12px; padding-bottom: 6px; border-bottom: 1px solid var(--color-border-tertiary); }
.accounts { display: flex; gap: 20px; flex-wrap: wrap; }
.account { flex: 1; min-width: 200px; }
.acct-title { font-size: 13px; font-weight: 500; text-align: center; margin-bottom: 4px; }
.t-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.t-table thead th { font-weight: 400; font-size: 10px; color: var(--color-text-tertiary); padding: 2px 6px 4px; }
.t-table thead th:first-child { text-align: left; }
.t-table thead th:last-child { text-align: right; }
.t-head-line { border-bottom: 1.5px solid var(--color-text-primary); }
.t-table td { padding: 2px 6px; vertical-align: top; }
.t-table td:first-child { border-right: 0.5px solid var(--color-border-secondary); }
.t-table td:last-child { text-align: right; }
.t-table .total-row td { border-top: 1px solid var(--color-text-primary); font-weight: 500; padding-top: 5px; }
.note { font-size: 11px; color: var(--color-text-secondary); }
.delta { color: #1D9E75; font-weight: 500; }
.delta-neg { color: #A32D2D; font-weight: 500; }
.sep { border: none; border-top: 1px dashed var(--color-border-tertiary); margin: 20px 0; }
.scenario { padding: 12px 16px; border-radius: var(--border-radius-lg); background: var(--color-background-secondary); margin-bottom: 20px; font-size: 13px; line-height: 1.8; }
.callout { padding: 10px 14px; border-radius: var(--border-radius-lg); margin-top: 8px; margin-bottom: 10px; font-size: 12px; line-height: 1.6; }
.callout-coral { background: #FAECE7; color: #712B13; }
.callout-green { background: #E7FAF0; color: #0E5431; }
.callout-purple { background: #F0E7FA; color: #3C1364; }
@media (prefers-color-scheme: dark) {
  .callout-coral { background: #4A1B0C; color: #F0997B; }
  .callout-green { background: #0C3A20; color: #7BF0B0; }
  .callout-purple { background: #2A0C4A; color: #C07BF0; }
}
.saldi-bar { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 14px; padding: 8px 12px; border-radius: var(--border-radius-lg); background: var(--color-background-secondary); border: 0.5px solid var(--color-border-tertiary); font-size: 12px; }
.saldo-item { display: flex; gap: 5px; align-items: baseline; }
.saldo-label { color: var(--color-text-secondary); }
.saldo-val { font-weight: 500; }
.saldo-pos { color: #1D9E75; }
.saldo-zero { color: var(--color-text-tertiary); }
.saldo-sep { color: var(--color-border-secondary); }
.summary-grid { display: flex; gap: 14px; flex-wrap: wrap; margin-top: 12px; }
.summary-card { flex: 1; min-width: 140px; padding: 12px 14px; border-radius: var(--border-radius-lg); text-align: center; }
.sc-teal { background: #E1F5EE; color: #085041; }
.sc-purple { background: #EEEDFE; color: #3C3489; }
.sc-amber { background: #FAEEDA; color: #633806; }
@media (prefers-color-scheme: dark) {
  .sc-teal { background: #04342C; color: #5DCAA5; }
  .sc-purple { background: #26215C; color: #AFA9EC; }
  .sc-amber { background: #412402; color: #FAC775; }
}
.summary-card .label { font-size: 12px; font-weight: 500; margin-bottom: 3px; }
.summary-card .val { font-size: 18px; font-weight: 500; }
.summary-card .sub { font-size: 11px; margin-top: 2px; }
.loan-tag { display: inline-block; font-size: 10px; font-weight: 500; padding: 1px 5px; border-radius: 4px; margin-right: 3px; }
.tag-a { background: #D6E4F0; color: #1F3864; }
.tag-b { background: #E8D5F0; color: #3C1F64; }
@media (prefers-color-scheme: dark) {
  .tag-a { background: #1F3864; color: #A8C4E0; }
  .tag-b { background: #3C1F64; color: #D0A8E0; }
}
.principle-box { padding: 10px 14px; border-radius: var(--border-radius-lg); background: var(--color-background-secondary); border-left: 3px solid #2E75B6; margin-bottom: 16px; font-size: 12px; line-height: 1.6; }
.je-table { width: 100%; border-collapse: collapse; font-size: 12px; margin: 6px 0; }
.je-table td { padding: 2px 6px; }
.je-table .je-sum { border-top: 1.5px solid var(--color-text-primary); font-weight: 500; }
.netting-box { display: flex; gap: 12px; margin: 8px 0; flex-wrap: wrap; }
.netting-item { flex: 1; min-width: 180px; padding: 8px 12px; border-radius: 8px; font-size: 12px; }
.ni-green { background: #E7FAF0; color: #0E5431; }
.ni-red { background: #FDEAEA; color: #7A1D1D; }
.ni-grey { background: var(--color-background-secondary); }
@media (prefers-color-scheme: dark) {
  .ni-green { background: #0C3A20; color: #7BF0B0; }
  .ni-red { background: #3D0E0E; color: #F09B9B; }
}
"""


def transform_tags(text: str) -> str:
    """Convert <tag-a>X</tag-a> to <span class="loan-tag tag-a">X</span> etc.
    Also convert <delta>X</delta> and <delta-neg>X</delta-neg>."""
    import re
    text = re.sub(r'<tag-(\w+)>(.*?)</tag-\1>', r'<span class="loan-tag tag-\1">\2</span>', text)
    text = re.sub(r'<delta>(.*?)</delta>', r'<span class="delta">\1</span>', text)
    text = re.sub(r'<delta-neg>(.*?)</delta-neg>', r'<span class="delta-neg">\1</span>', text)
    text = re.sub(r'<note>(.*?)</note>', r'<span class="note">\1</span>', text)
    return text


def render_principles(principles: list[str]) -> str:
    lines = ['<div class="principle-box">', '<strong>Principper:</strong><br>']
    for i, p in enumerate(principles, 1):
        lines.append(f'{i}. {transform_tags(p)}<br>')
    lines.append('</div>')
    return '\n'.join(lines)


def render_scenario(scenario_html: str) -> str:
    return f'<div class="scenario">\n<strong>Scenarie:</strong><br>\n{transform_tags(scenario_html)}\n</div>'


def render_callout(callout: dict) -> str:
    color_map = {"green": "callout-green", "coral": "callout-coral", "red": "callout-coral", "purple": "callout-purple"}
    css = color_map.get(callout.get("color", "green"), "callout-green")
    return f'<div class="callout {css}">\n{transform_tags(callout["html"])}\n</div>'


def render_netting(items: list[dict]) -> str:
    color_map = {"green": "ni-green", "red": "ni-red", "grey": "ni-grey"}
    parts = ['<div class="netting-box">']
    for item in items:
        css = color_map.get(item.get("color", "grey"), "ni-grey")
        parts.append(f'<div class="netting-item {css}">{transform_tags(item["html"])}</div>')
    parts.append('</div>')
    return '\n'.join(parts)


def render_account(acct: dict) -> str:
    lines = [
        '<div class="account">',
        f'<div class="acct-title">{transform_tags(acct["title"])}</div>',
        '<table class="t-table">',
        '<thead><tr class="t-head-line"><th>Debet</th><th>Kredit</th></tr></thead>',
        '<tbody>'
    ]
    for row in acct.get("rows", []):
        if row.get("total"):
            d = transform_tags(row.get("debet_total", ""))
            k = transform_tags(row.get("kredit_total", ""))
            lines.append(f'<tr class="total-row"><td>{d}</td><td>{k}</td></tr>')
        else:
            d = transform_tags(row.get("debet", ""))
            k = transform_tags(row.get("kredit", ""))
            lines.append(f'<tr><td>{d}</td><td>{k}</td></tr>')
    lines.extend(['</tbody>', '</table>', '</div>'])
    return '\n'.join(lines)


def render_saldi_bar(items: list[dict]) -> str:
    parts = ['<div class="saldi-bar">']
    for i, item in enumerate(items):
        css = item.get("css", "")
        parts.append(f'<div class="saldo-item"><span class="saldo-label">{item["label"]}:</span> <span class="saldo-val {css}">{item["value"]}</span></div>')
        if i < len(items) - 1:
            parts.append('<span class="saldo-sep">|</span>')
    parts.append('</div>')
    return '\n'.join(parts)


def render_day(day: dict) -> str:
    lines = ['<div class="day">', f'<div class="day-title">{transform_tags(day["title"])}</div>']
    for c in day.get("callouts", []):
        lines.append(render_callout(c))
    if day.get("netting"):
        lines.append(render_netting(day["netting"]))
    lines.append('<div class="accounts">')
    for acct in day.get("accounts", []):
        lines.append(render_account(acct))
    lines.append('</div>')
    if day.get("saldi"):
        lines.append(render_saldi_bar(day["saldi"]))
    lines.append('</div>')
    return '\n'.join(lines)


def render_summary_cards(cards: list[dict]) -> str:
    lines = ['<div class="summary-grid">']
    for card in cards:
        color = card.get("color", "teal")
        lines.append(f'<div class="summary-card sc-{color}">')
        lines.append(f'<div class="label">{card["label"]}</div>')
        lines.append(f'<div class="val">{card["value"]}</div>')
        if card.get("sub"):
            lines.append(f'<div class="sub">{card["sub"]}</div>')
        lines.append('</div>')
    lines.append('</div>')
    return '\n'.join(lines)


def render_netting_table(table: dict) -> str:
    lines = ['<div class="principle-box">', '<table class="je-table">']
    # Header
    headers = table.get("headers", [])
    if headers:
        lines.append('<tr style="color:var(--color-text-tertiary)">')
        for i, h in enumerate(headers):
            style = 'style="text-align:right; width:90px; font-size:10px"' if i > 0 else 'style="padding-left:14px"'
            if i == len(headers) - 1:
                style = 'style="text-align:right; width:70px; font-size:10px"'
            bold = "<strong>" if i == len(headers) - 1 else ""
            bold_end = "</strong>" if i == len(headers) - 1 else ""
            lines.append(f'<td {style}>{bold}{h}{bold_end}</td>')
        lines.append('</tr>')
    # Sections
    for section in table.get("sections", []):
        lines.append(f'<tr><td style="padding-left:14px" colspan="{len(headers)}"><em>{section["title"]}</em></td></tr>')
        for row in section.get("rows", []):
            lines.append('<tr>')
            for i, cell in enumerate(row):
                style = 'style="padding-left:28px"' if i == 0 else 'style="text-align:right"'
                bold = "<strong>" if i == len(row) - 1 else ""
                bold_end = "</strong>" if i == len(row) - 1 else ""
                lines.append(f'<td {style}>{bold}{cell}{bold_end}</td>')
            lines.append('</tr>')
    # Total
    total = table.get("total")
    if total:
        lines.append('<tr class="je-sum">')
        for i, cell in enumerate(total):
            style = 'style="padding-top:5px"' if i == 0 else 'style="text-align:right; padding-top:5px"' if i == len(total) - 1 else ''
            lines.append(f'<td {style}><strong>{cell}</strong></td>')
        lines.append('</tr>')
    lines.extend(['</table>', '</div>'])
    return '\n'.join(lines)


def render_conclusion(text: str) -> str:
    return f'<div class="principle-box" style="border-left-color: #1D9E75;">\n<strong>Konklusion:</strong> {transform_tags(text)}\n</div>'


def generate_html(data: dict) -> str:
    parts = [
        '<!DOCTYPE html>',
        '<html lang="da">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f'<title>{html_module.escape(data.get("title", "IFRS 9 T-konti"))}</title>',
        f'<style>{CSS}</style>',
        '</head>',
        '<body>',
        f'<h1>{html_module.escape(data.get("title", ""))}</h1>',
    ]
    if data.get("subtitle"):
        parts.append(f'<p class="subtitle">{html_module.escape(data["subtitle"])}</p>')
    if data.get("principles"):
        parts.append(render_principles(data["principles"]))
    if data.get("scenario"):
        parts.append(render_scenario(data["scenario"]))
    for i, day in enumerate(data.get("days", [])):
        if i > 0:
            parts.append('<hr class="sep">')
        parts.append(render_day(day))
    if data.get("summary_cards") or data.get("netting_table") or data.get("conclusion"):
        parts.append('<hr class="sep">')
    if data.get("summary_cards"):
        parts.append('<div class="day-title">Opsummering</div>')
        parts.append(render_summary_cards(data["summary_cards"]))
    if data.get("netting_table"):
        parts.append('<hr class="sep">')
        parts.append('<div class="day-title">Netting-oversigt</div>')
        parts.append(render_netting_table(data["netting_table"]))
    if data.get("conclusion"):
        parts.append(render_conclusion(data["conclusion"]))
    parts.extend(['</body>', '</html>'])
    return '\n'.join(parts)


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/generate_tkonti.py input.json output.html")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    html_output = generate_html(data)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_output)

    print(f"✅ Generated {output_path} ({len(html_output):,} bytes)")


if __name__ == '__main__':
    main()
