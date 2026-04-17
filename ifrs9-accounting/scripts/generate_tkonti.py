#!/usr/bin/env python3
"""
generate_tkonti.py — Generates IFRS 9 T-konti HTML from JSON input.

Usage:
    python scripts/generate_tkonti.py input.json output.html

---

INPUT JSON SCHEMA (v2 — strict types)

Breaking change from v1: debet/kredit are now NUMBERS, not strings.
All amounts are typed. The script handles all formatting (Danish thousand-separator,
signs, colors). Claude only writes numbers.

---

Top-level structure:

{
  "title":          str  (required)
  "subtitle":       str  (optional)
  "principles":     [str, ...]  (optional, 4-7 recommended)
  "scenario":       str  (optional, HTML with <tag-a>/<tag-b> markup)
  "days":           [Day, ...]  (required)
  "summary_cards":  [SummaryCard, ...]  (optional)
  "netting_table":  NettingTable  (optional)
  "conclusion":     str  (optional)
}

---

Day:

{
  "title":    str  (required)
  "callouts": [Callout, ...]  (optional)
  "netting":  [NettingItem, ...]  (optional)
  "accounts": [Account, ...]  (required)
  "saldi":    [SaldoItem, ...]  (optional)
}

Callout:
  {"color": "green"|"coral"|"red"|"purple", "html": str}
  Use <strong>, <tag-a>, <tag-b>, <note> in html.

NettingItem (one of two forms):
  Typed:   {"label": str, "amount": number}         color from sign (+ green, − red, 0 grey)
  Free:    {"color": "green"|"red"|"grey", "html": str}   legacy-style explicit

Account:
  {"title": str, "rows": [Row, ...]}

Row (one of three kinds):
  Posting debit:    {"text": str, "debet": number}
  Posting credit:   {"text": str, "kredit": number}
  Total:            {"total": true, "saldo": number, "side": "debet"|"kredit"}

  Rules:
  - A posting row has EXACTLY one of debet OR kredit, never both, never neither
  - debet/kredit MUST be numbers (int or float), never strings
  - text is optional but recommended (one or two words like "Oprettelse", "Afdrag")
  - Total row shows saldo on the specified side; the other side is blank

SaldoItem:
  Typed number:  {"label": str, "value": number}    formatted + color from sign
  Free string:   {"label": str, "value": str}       used for "✓" checkmarks etc.

---

SummaryCard:
  {
    "label": str,
    "value": number|str,     number formatted Danish; string used as-is
    "sub":   str (optional),
    "color": "teal"|"purple"|"amber"
  }

NettingTable:
  {
    "headers": [str, ...],
    "sections": [{"title": str, "rows": [[cell, ...], ...]}, ...],
    "total":    [cell, ...] (optional)
  }
  Cell can be number (formatted Danish + color by sign) or string (used as-is).

---

Markup in str fields:
  <tag-a>X</tag-a>    blue loan tag
  <tag-b>X</tag-b>    purple loan tag
  <strong>X</strong>  bold
  <note>X</note>      small grey note

Numbers are formatted by the script: 994000 → "994.000", -21500 → "−21.500".
"""

import html as html_module
import json
import re
import sys


# ============================================================================
# Number formatting (Danish: 994.000, −21.500)
# ============================================================================

def is_number(x) -> bool:
    """True if x is int/float but not bool."""
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def format_amount(n: float, show_plus: bool = False) -> str:
    """Format a number Danish-style with U+2212 minus.

    Examples:
        994000, False  → '994.000'
        -21500, False  → '−21.500'
        21500, True    → '+21.500'
        0, *           → '0'
    """
    if n == 0:
        return "0"
    sign_char = ""
    abs_n = n
    if n < 0:
        sign_char = "−"  # U+2212
        abs_n = -n
    elif show_plus:
        sign_char = "+"
    if isinstance(abs_n, int) or abs_n == int(abs_n):
        body = f"{int(abs_n):,}".replace(",", ".")
    else:
        body = f"{abs_n:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")
    return sign_char + body


def color_class_for_sign(n: float, neutral_is_grey: bool = True) -> str:
    if n > 0:
        return "delta"
    if n < 0:
        return "delta-neg"
    return "saldo-zero" if neutral_is_grey else ""


# ============================================================================
# Markup transformation (only tags; amounts are typed)
# ============================================================================

_TAG_RE = re.compile(r"<tag-(\w+)>(.*?)</tag-\1>")
_NOTE_RE = re.compile(r"<note>(.*?)</note>")


def transform_markup(text: str) -> str:
    if not text:
        return ""
    text = _TAG_RE.sub(r'<span class="loan-tag tag-\1">\2</span>', text)
    text = _NOTE_RE.sub(r'<span class="note">\1</span>', text)
    return text


def _require(cond: bool, msg: str) -> None:
    if not cond:
        raise ValueError(f"Schema error: {msg}")


# ============================================================================
# CSS loading (from sibling assets/tkonti.css)
# ============================================================================

def _script_dir() -> str:
    """Return the directory containing this script."""
    import os
    return os.path.dirname(os.path.abspath(__file__))


def load_css() -> str:
    """Load CSS from assets/tkonti.css relative to the skill root.

    Expected layout:
        skill-root/
          scripts/generate_tkonti.py
          assets/tkonti.css

    Raises FileNotFoundError with a clear message if not found.
    """
    import os
    script_dir = _script_dir()
    # Try standard layout: ../assets/tkonti.css
    candidates = [
        os.path.join(script_dir, "..", "assets", "tkonti.css"),
        os.path.join(script_dir, "assets", "tkonti.css"),  # same-dir layout
        os.path.join(script_dir, "tkonti.css"),             # next to script
    ]
    for path in candidates:
        norm = os.path.normpath(path)
        if os.path.isfile(norm):
            with open(norm, encoding="utf-8") as f:
                return f.read()
    tried = "\n  ".join(os.path.normpath(c) for c in candidates)
    raise FileNotFoundError(
        f"Could not find assets/tkonti.css. Looked in:\n  {tried}\n"
        f"Ensure the skill structure is intact."
    )


# ============================================================================
# Renderers
# ============================================================================

def render_principles(principles: list) -> str:
    lines = ['<div class="principle-box">', '<strong>Principper:</strong><br>']
    for i, p in enumerate(principles, 1):
        lines.append(f'{i}. {transform_markup(p)}<br>')
    lines.append('</div>')
    return '\n'.join(lines)


def render_scenario(scenario_html: str) -> str:
    return f'<div class="scenario">\n<strong>Scenarie:</strong><br>\n{transform_markup(scenario_html)}\n</div>'


def render_callout(callout: dict) -> str:
    color_map = {"green": "callout-green", "coral": "callout-coral",
                 "red": "callout-coral", "purple": "callout-purple"}
    css = color_map.get(callout.get("color", "green"), "callout-green")
    return f'<div class="callout {css}">\n{transform_markup(callout["html"])}\n</div>'


def render_netting(items: list) -> str:
    """Two forms supported:
    - Typed: {"label": str, "amount": number}
    - Free:  {"color": ..., "html": str}
    """
    color_map = {"green": "ni-green", "red": "ni-red", "grey": "ni-grey"}
    parts = ['<div class="netting-box">']
    for item in items:
        if "amount" in item:
            amt = item["amount"]
            _require(is_number(amt), f"netting amount must be number, got {type(amt).__name__}")
            if amt > 0:
                css = "ni-green"
                show_plus = True
            elif amt < 0:
                css = "ni-red"
                show_plus = False
            else:
                css = "ni-grey"
                show_plus = False
            label = transform_markup(item.get("label", ""))
            formatted = format_amount(amt, show_plus=show_plus)
            label_part = f"{label}: " if label else ""
            parts.append(f'<div class="netting-item {css}">{label_part}<strong>{formatted}</strong></div>')
        else:
            css = color_map.get(item.get("color", "grey"), "ni-grey")
            parts.append(f'<div class="netting-item {css}">{transform_markup(item["html"])}</div>')
    parts.append('</div>')
    return '\n'.join(parts)


def _format_posting_cell(text: str, amount: float) -> str:
    parts = []
    if text:
        parts.append(transform_markup(text))
    parts.append(format_amount(amount))
    return " ".join(parts)


def render_account(acct: dict) -> str:
    _require("title" in acct, "account missing 'title'")
    rows = acct.get("rows", [])
    title = acct["title"]
    lines = [
        '<div class="account">',
        f'<div class="acct-title">{transform_markup(title)}</div>',
        '<table class="t-table">',
        '<thead><tr class="t-head-line"><th>Debet</th><th>Kredit</th></tr></thead>',
        '<tbody>'
    ]
    for i, row in enumerate(rows):
        if row.get("total"):
            saldo = row.get("saldo", 0)
            _require(is_number(saldo), f"'{title}' total row {i}: saldo must be number")
            side = row.get("side", "debet")
            _require(side in ("debet", "kredit"),
                     f"'{title}' total row {i}: side must be 'debet' or 'kredit'")
            saldo_text = f"Saldo: {format_amount(saldo)}"
            if side == "debet":
                lines.append(f'<tr class="total-row"><td>{saldo_text}</td><td></td></tr>')
            else:
                lines.append(f'<tr class="total-row"><td></td><td>{saldo_text}</td></tr>')
        else:
            has_d = "debet" in row
            has_k = "kredit" in row
            _require(has_d ^ has_k,
                     f"'{title}' row {i}: must have exactly one of 'debet' or 'kredit' "
                     f"(got debet={has_d}, kredit={has_k})")
            text = row.get("text", "")
            if has_d:
                amt = row["debet"]
                _require(is_number(amt),
                         f"'{title}' row {i}: debet must be number, got {type(amt).__name__}: {amt!r}")
                lines.append(f'<tr><td>{_format_posting_cell(text, amt)}</td><td></td></tr>')
            else:
                amt = row["kredit"]
                _require(is_number(amt),
                         f"'{title}' row {i}: kredit must be number, got {type(amt).__name__}: {amt!r}")
                lines.append(f'<tr><td></td><td>{_format_posting_cell(text, amt)}</td></tr>')
    lines.extend(['</tbody>', '</table>', '</div>'])
    return '\n'.join(lines)


def render_saldi_bar(items: list) -> str:
    parts = ['<div class="saldi-bar">']
    for i, item in enumerate(items):
        _require("label" in item and "value" in item,
                 f"saldi item {i}: missing 'label' or 'value'")
        value = item["value"]
        if is_number(value):
            css = color_class_for_sign(value)
            formatted = format_amount(value, show_plus=(value > 0))
        else:
            css = item.get("css", "")
            formatted = str(value)
        parts.append(
            f'<div class="saldo-item"><span class="saldo-label">{item["label"]}:</span> '
            f'<span class="saldo-val {css}">{formatted}</span></div>'
        )
        if i < len(items) - 1:
            parts.append('<span class="saldo-sep">|</span>')
    parts.append('</div>')
    return '\n'.join(parts)


def render_day(day: dict) -> str:
    _require("title" in day, "day missing 'title'")
    lines = ['<div class="day">', f'<div class="day-title">{transform_markup(day["title"])}</div>']
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


def render_summary_cards(cards: list) -> str:
    lines = ['<div class="summary-grid">']
    for card in cards:
        color = card.get("color", "teal")
        value = card.get("value", "")
        if is_number(value):
            formatted = format_amount(value, show_plus=(value > 0))
        else:
            formatted = str(value)
        lines.append(f'<div class="summary-card sc-{color}">')
        lines.append(f'<div class="label">{transform_markup(card.get("label", ""))}</div>')
        lines.append(f'<div class="val">{formatted}</div>')
        if card.get("sub"):
            lines.append(f'<div class="sub">{transform_markup(card["sub"])}</div>')
        lines.append('</div>')
    lines.append('</div>')
    return '\n'.join(lines)


def _format_table_cell(cell) -> str:
    if is_number(cell):
        css = color_class_for_sign(cell, neutral_is_grey=False)
        formatted = format_amount(cell, show_plus=(cell > 0))
        if css:
            return f'<span class="{css}">{formatted}</span>'
        return formatted
    return str(cell)


def render_netting_table(table: dict) -> str:
    lines = ['<div class="principle-box">', '<table class="je-table">']
    headers = table.get("headers", [])
    if headers:
        lines.append('<tr style="color:var(--color-text-tertiary)">')
        for i, h in enumerate(headers):
            if i == 0:
                style = 'style="padding-left:14px"'
            elif i == len(headers) - 1:
                style = 'style="text-align:right; width:70px; font-size:10px"'
            else:
                style = 'style="text-align:right; width:90px; font-size:10px"'
            if i == len(headers) - 1:
                lines.append(f'<td {style}><strong>{h}</strong></td>')
            else:
                lines.append(f'<td {style}>{h}</td>')
        lines.append('</tr>')
    for section in table.get("sections", []):
        lines.append(f'<tr><td style="padding-left:14px" colspan="{len(headers)}"><em>{section["title"]}</em></td></tr>')
        for row in section.get("rows", []):
            lines.append('<tr>')
            for i, cell in enumerate(row):
                style = 'style="padding-left:28px"' if i == 0 else 'style="text-align:right"'
                formatted = _format_table_cell(cell)
                if i == len(row) - 1:
                    formatted = f'<strong>{formatted}</strong>'
                lines.append(f'<td {style}>{formatted}</td>')
            lines.append('</tr>')
    total = table.get("total")
    if total:
        lines.append('<tr class="je-sum">')
        for i, cell in enumerate(total):
            if i == 0:
                style = 'style="padding-top:5px"'
            else:
                style = 'style="text-align:right; padding-top:5px"'
            formatted = _format_table_cell(cell)
            lines.append(f'<td {style}><strong>{formatted}</strong></td>')
        lines.append('</tr>')
    lines.extend(['</table>', '</div>'])
    return '\n'.join(lines)


def render_conclusion(text: str) -> str:
    return f'<div class="principle-box" style="border-left-color: #1D9E75;">\n<strong>Konklusion:</strong> {transform_markup(text)}\n</div>'


def generate_html(data: dict) -> str:
    _require("title" in data, "top-level 'title' required")
    _require("days" in data and isinstance(data["days"], list),
             "top-level 'days' array required")

    parts = [
        '<!DOCTYPE html>',
        '<html lang="da">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f'<title>{html_module.escape(data["title"])}</title>',
        f'<style>{load_css()}</style>',
        '</head>',
        '<body>',
        f'<h1>{html_module.escape(data["title"])}</h1>',
    ]
    if data.get("subtitle"):
        parts.append(f'<p class="subtitle">{html_module.escape(data["subtitle"])}</p>')
    if data.get("principles"):
        parts.append(render_principles(data["principles"]))
    if data.get("scenario"):
        parts.append(render_scenario(data["scenario"]))
    for i, day in enumerate(data["days"]):
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
        print("Usage: python scripts/generate_tkonti.py input.json output.html", file=sys.stderr)
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    try:
        html_output = generate_html(data)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_output)
    print(f"✅ Generated {output_path} ({len(html_output):,} bytes)")


if __name__ == '__main__':
    main()
