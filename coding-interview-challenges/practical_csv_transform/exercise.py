"""
Exercise: read CSV, filter rows, add computed column, write CSV.
Fill in the TODOs. See README.md for the problem description.
"""

import csv
from pathlib import Path


def load_csv(path: str) -> list[dict[str, str]]:
    """Read CSV with header; return list of dicts (one per row)."""
    rows = []
    # TODO: open path, use csv.DictReader; append each row to rows
    # TODO: handle FileNotFoundError: print message and return []
    return rows


def filter_rows(
    rows: list[dict[str, str]], region: str
) -> list[dict[str, str]]:
    """Return rows where 'region' equals the given value."""
    # TODO: return [r for r in rows if r.get("region") == region]
    return []


def add_computed_column(
    rows: list[dict[str, str]], cost_key: str = "cost", tax_rate: float = 1.1
) -> list[dict[str, str]]:
    """Add cost_with_tax = cost * tax_rate. Cost may be string; convert to float."""
    # TODO: for each row, cost = float(row.get(cost_key, 0)); row["cost_with_tax"] = round(cost * tax_rate, 2)
    # TODO: return rows (modified in place or new list)
    return rows


def write_csv(path: str, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    """Write rows to CSV with the given column order."""
    # TODO: open path for writing, csv.DictWriter with fieldnames, writeheader(), writerows(rows)
    pass


def main() -> None:
    base = Path(__file__).parent
    inp = base / "input.csv"
    out = base / "output.csv"
    rows = load_csv(str(inp))
    if not rows:
        print("No rows loaded.")
        return
    filtered = filter_rows(rows, "us-east")
    with_tax = add_computed_column(filtered)
    fieldnames = ["name", "region", "cost", "cost_with_tax"]
    write_csv(str(out), with_tax, fieldnames)
    print(f"Wrote {len(with_tax)} rows to {out}")


if __name__ == "__main__":
    main()
