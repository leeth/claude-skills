#!/usr/bin/env python3
"""
validate_scenario.py — Validate IFRS 9 T-konti JSON input (v2 schema).

The v2 schema has typed amounts, so balance checks are exact (no regex).

Checks:
  - Required fields (title, days)
  - Recommended fields (subtitle, principles, scenario, conclusion)
  - days[*]: title, accounts
  - accounts[*]: title, rows
  - rows[*]: exactly one of debet/kredit (numbers), OR total=true
  - total rows: saldo (number) + side ('debet'|'kredit')
  - Balance: for every account, Σ debet − Σ kredit == declared saldo (respecting side)
  - Cross-account: optionally, if saldi-bar contains a balance check, validate it
  - Color tokens for callouts, netting, summary_cards
  - Netting items: exactly one of typed {label, amount} or free {color, html}
  - Netting_table: headers/rows/total cell counts align

Exit codes:
  0 = OK (possibly with warnings unless --strict)
  1 = validation errors
  2 = file/JSON error

Usage:
  python scripts/validate_scenario.py input.json
  python scripts/validate_scenario.py input.json --strict
"""

import json
import sys
from dataclasses import dataclass, field


VALID_CALLOUT_COLORS = {"green", "coral", "red", "purple"}
VALID_NETTING_COLORS = {"green", "red", "grey"}
VALID_SALDO_CSS = {"", "saldo-pos", "saldo-zero", "saldo-neg", "delta", "delta-neg"}
VALID_CARD_COLORS = {"teal", "purple", "amber"}

REQUIRED_TOP = ["title", "days", "legal_framework"]
RECOMMENDED_TOP = ["subtitle", "principles", "scenario", "conclusion"]


@dataclass
class Result:
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def print_report(self) -> None:
        if self.errors:
            print(f"❌ {len(self.errors)} error(s):", file=sys.stderr)
            for e in self.errors:
                print(f"  • {e}", file=sys.stderr)
        if self.warnings:
            print(f"⚠️  {len(self.warnings)} warning(s):", file=sys.stderr)
            for w in self.warnings:
                print(f"  • {w}", file=sys.stderr)
        if self.ok and not self.warnings:
            print("✅ JSON valid and balanced")
        elif self.ok:
            print(f"✅ JSON valid ({len(self.warnings)} warnings)")


def is_number(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def validate_top(data: dict, r: Result) -> None:
    if not isinstance(data, dict):
        r.errors.append("Root must be an object")
        return
    for f in REQUIRED_TOP:
        if f not in data:
            r.errors.append(f"Missing required top-level field: '{f}'")
    for f in RECOMMENDED_TOP:
        if f not in data:
            r.warnings.append(f"Recommended top-level field missing: '{f}'")
    if "days" in data and not isinstance(data["days"], list):
        r.errors.append("'days' must be an array")
    if "principles" in data:
        ps = data["principles"]
        if not isinstance(ps, list):
            r.errors.append("'principles' must be an array of strings")
        elif len(ps) < 3:
            r.warnings.append(f"Only {len(ps)} principle(s) — aim for 4-7 for completeness")


def validate_account(acct: dict, day_idx: int, acct_idx: int, r: Result) -> None:
    loc = f"day[{day_idx}].accounts[{acct_idx}]"
    if not isinstance(acct, dict):
        r.errors.append(f"{loc}: must be an object")
        return
    title = acct.get("title", "?")
    if "title" not in acct:
        r.errors.append(f"{loc}: missing 'title'")

    rows = acct.get("rows", [])
    if not isinstance(rows, list):
        r.errors.append(f"{loc}: 'rows' must be an array")
        return

    debit_sum = 0.0
    credit_sum = 0.0
    declared_saldo = None
    declared_side = None
    total_row_count = 0

    for i, row in enumerate(rows):
        row_loc = f"{loc}('{title}').rows[{i}]"
        if not isinstance(row, dict):
            r.errors.append(f"{row_loc}: must be an object")
            continue

        if row.get("total"):
            total_row_count += 1
            saldo = row.get("saldo")
            if not is_number(saldo):
                r.errors.append(f"{row_loc}: total row 'saldo' must be a number")
                continue
            side = row.get("side")
            if side not in ("debet", "kredit"):
                r.errors.append(f"{row_loc}: total row 'side' must be 'debet' or 'kredit' (got {side!r})")
                continue
            declared_saldo = saldo
            declared_side = side
            # Forbid debet/kredit keys on total rows
            if "debet" in row or "kredit" in row:
                r.warnings.append(f"{row_loc}: total row should not have 'debet'/'kredit' keys; use 'saldo'+'side'")
            continue

        # Posting row
        has_d = "debet" in row
        has_k = "kredit" in row
        if has_d == has_k:
            r.errors.append(
                f"{row_loc}: posting row must have EXACTLY one of 'debet' or 'kredit' "
                f"(got debet={has_d}, kredit={has_k})"
            )
            continue
        if has_d:
            amt = row["debet"]
            if not is_number(amt):
                r.errors.append(f"{row_loc}: 'debet' must be a number, got {type(amt).__name__}: {amt!r}")
                continue
            debit_sum += amt
        else:
            amt = row["kredit"]
            if not is_number(amt):
                r.errors.append(f"{row_loc}: 'kredit' must be a number, got {type(amt).__name__}: {amt!r}")
                continue
            credit_sum += amt

    if total_row_count > 1:
        r.warnings.append(f"{loc}('{title}'): {total_row_count} total rows found — typically one per account")
    if total_row_count == 0:
        r.warnings.append(f"{loc}('{title}'): no total row — UI will not show a saldo line")

    # Balance check
    if declared_saldo is not None:
        net = debit_sum - credit_sum
        expected_net = declared_saldo if declared_side == "debet" else -declared_saldo
        if abs(net - expected_net) > 0.01:
            r.errors.append(
                f"{loc}('{title}'): BALANCE ERROR — Σ Dr ({debit_sum:,.2f}) − Σ Cr ({credit_sum:,.2f}) "
                f"= {net:,.2f}, but declared saldo is {declared_saldo:,.2f} on {declared_side} side "
                f"(expected net {expected_net:,.2f})"
            )


def validate_callouts(day: dict, idx: int, r: Result) -> None:
    for i, c in enumerate(day.get("callouts", [])):
        loc = f"day[{idx}].callouts[{i}]"
        if not isinstance(c, dict):
            r.errors.append(f"{loc}: must be an object")
            continue
        if "html" not in c:
            r.errors.append(f"{loc}: missing 'html'")
        color = c.get("color", "green")
        if color not in VALID_CALLOUT_COLORS:
            r.errors.append(f"{loc}: invalid color '{color}'. Valid: {sorted(VALID_CALLOUT_COLORS)}")


def validate_netting(day: dict, idx: int, r: Result) -> None:
    for i, n in enumerate(day.get("netting", [])):
        loc = f"day[{idx}].netting[{i}]"
        if not isinstance(n, dict):
            r.errors.append(f"{loc}: must be an object")
            continue
        has_amount = "amount" in n
        has_html = "html" in n
        if has_amount == has_html:
            r.errors.append(
                f"{loc}: must have EXACTLY one of typed form {{'label','amount'}} "
                f"OR free form {{'color','html'}} (got amount={has_amount}, html={has_html})"
            )
            continue
        if has_amount:
            if not is_number(n["amount"]):
                r.errors.append(f"{loc}: 'amount' must be a number, got {type(n['amount']).__name__}")
        else:
            color = n.get("color", "grey")
            if color not in VALID_NETTING_COLORS:
                r.errors.append(f"{loc}: invalid color '{color}'. Valid: {sorted(VALID_NETTING_COLORS)}")


def validate_saldi(day: dict, idx: int, r: Result) -> None:
    for i, s in enumerate(day.get("saldi", [])):
        loc = f"day[{idx}].saldi[{i}]"
        if not isinstance(s, dict):
            r.errors.append(f"{loc}: must be an object")
            continue
        if "label" not in s or "value" not in s:
            r.errors.append(f"{loc}: missing 'label' or 'value'")
        v = s.get("value")
        if not (is_number(v) or isinstance(v, str)):
            r.errors.append(f"{loc}: 'value' must be number or string, got {type(v).__name__}")
        css = s.get("css", "")
        if css not in VALID_SALDO_CSS:
            r.warnings.append(f"{loc}: unknown css '{css}'. Valid: {sorted(VALID_SALDO_CSS)}")


def validate_day(day: dict, idx: int, r: Result) -> None:
    loc = f"day[{idx}]"
    if not isinstance(day, dict):
        r.errors.append(f"{loc}: must be an object")
        return
    if "title" not in day:
        r.errors.append(f"{loc}: missing 'title'")
    validate_callouts(day, idx, r)
    validate_netting(day, idx, r)

    accounts = day.get("accounts", [])
    if not isinstance(accounts, list):
        r.errors.append(f"{loc}.accounts: must be an array")
    elif len(accounts) == 0:
        r.warnings.append(f"{loc}: no accounts — day will render empty")
    else:
        for i, acct in enumerate(accounts):
            validate_account(acct, idx, i, r)

    validate_saldi(day, idx, r)


def validate_summary_cards(cards: list, r: Result) -> None:
    if not isinstance(cards, list):
        r.errors.append("'summary_cards' must be an array")
        return
    for i, c in enumerate(cards):
        loc = f"summary_cards[{i}]"
        if not isinstance(c, dict):
            r.errors.append(f"{loc}: must be an object")
            continue
        if "label" not in c or "value" not in c:
            r.errors.append(f"{loc}: missing 'label' or 'value'")
        v = c.get("value")
        if not (is_number(v) or isinstance(v, str)):
            r.errors.append(f"{loc}: 'value' must be number or string")
        color = c.get("color", "teal")
        if color not in VALID_CARD_COLORS:
            r.warnings.append(f"{loc}: unknown color '{color}'. Valid: {sorted(VALID_CARD_COLORS)}")


def validate_netting_table(table: dict, r: Result) -> None:
    if not isinstance(table, dict):
        r.errors.append("'netting_table' must be an object")
        return
    headers = table.get("headers", [])
    if not isinstance(headers, list):
        r.errors.append("netting_table.headers must be an array")
        headers = []
    sections = table.get("sections", [])
    if not isinstance(sections, list):
        r.errors.append("netting_table.sections must be an array")
        sections = []
    n_cols = len(headers)
    for i, s in enumerate(sections):
        loc = f"netting_table.sections[{i}]"
        if not isinstance(s, dict):
            r.errors.append(f"{loc}: must be an object")
            continue
        if "title" not in s:
            r.errors.append(f"{loc}: missing 'title'")
        for j, row in enumerate(s.get("rows", [])):
            if not isinstance(row, list):
                r.errors.append(f"{loc}.rows[{j}]: must be an array")
            elif n_cols > 0 and len(row) != n_cols:
                r.errors.append(f"{loc}.rows[{j}]: has {len(row)} cells but table has {n_cols} headers")
    total = table.get("total")
    if total is not None:
        if not isinstance(total, list):
            r.errors.append("netting_table.total must be an array")
        elif n_cols > 0 and len(total) != n_cols:
            r.errors.append(f"netting_table.total: has {len(total)} cells but table has {n_cols} headers")


def validate_legal_framework(lf, r: Result) -> None:
    if not isinstance(lf, dict):
        r.errors.append("'legal_framework' must be an object")
        return
    sources = lf.get("sources")
    if not isinstance(sources, list) or len(sources) == 0:
        r.errors.append("legal_framework.sources must be a non-empty array")
        return
    for i, src in enumerate(sources):
        loc = f"legal_framework.sources[{i}]"
        if not isinstance(src, dict):
            r.errors.append(f"{loc}: must be an object")
            continue
        if "source" not in src:
            r.errors.append(f"{loc}: missing 'source' (short name, e.g. 'IFRS 9')")
        paragraphs = src.get("paragraphs")
        if not isinstance(paragraphs, list) or len(paragraphs) == 0:
            r.errors.append(f"{loc}: 'paragraphs' must be a non-empty array")
            continue
        for j, p in enumerate(paragraphs):
            ploc = f"{loc}.paragraphs[{j}]"
            if not isinstance(p, dict):
                r.errors.append(f"{ploc}: must be an object with 'ref' and 'note'")
                continue
            if "ref" not in p or not isinstance(p["ref"], str) or not p["ref"].strip():
                r.errors.append(f"{ploc}: 'ref' must be a non-empty string (e.g. 'B5.1.2A', '§ 20, stk. 3')")
            if "note" in p and not isinstance(p["note"], str):
                r.errors.append(f"{ploc}: 'note' must be a string when present")

    choices = lf.get("interpretive_choices")
    if choices is not None:
        if not isinstance(choices, list):
            r.errors.append("legal_framework.interpretive_choices must be an array of strings")
        else:
            for i, c in enumerate(choices):
                if not isinstance(c, str):
                    r.errors.append(f"legal_framework.interpretive_choices[{i}]: must be a string")

    not_applied = lf.get("not_applied")
    if not_applied is not None:
        if not isinstance(not_applied, list):
            r.errors.append("legal_framework.not_applied must be an array")
        else:
            for i, item in enumerate(not_applied):
                loc = f"legal_framework.not_applied[{i}]"
                if isinstance(item, dict):
                    if "source" not in item and "note" not in item:
                        r.errors.append(f"{loc}: must have at least 'source' or 'note'")
                elif not isinstance(item, str):
                    r.errors.append(f"{loc}: must be an object {{source, note}} or a string")


def validate(data: dict) -> Result:
    r = Result()
    validate_top(data, r)
    if r.errors:
        return r
    for i, day in enumerate(data.get("days", [])):
        validate_day(day, i, r)
    if "summary_cards" in data:
        validate_summary_cards(data["summary_cards"], r)
    if "netting_table" in data:
        validate_netting_table(data["netting_table"], r)
    if "legal_framework" in data:
        validate_legal_framework(data["legal_framework"], r)
    return r


def main() -> int:
    args = sys.argv[1:]
    strict = "--strict" in args
    args = [a for a in args if not a.startswith("--")]
    if len(args) < 1:
        print("Usage: python scripts/validate_scenario.py input.json [--strict]", file=sys.stderr)
        return 2
    path = args[0]
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}", file=sys.stderr)
        return 2
    result = validate(data)
    result.print_report()
    if result.errors:
        return 1
    if strict and result.warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
