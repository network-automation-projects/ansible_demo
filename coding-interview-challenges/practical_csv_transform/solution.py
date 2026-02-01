"""
CSV transform: read CSV, filter by region, add cost_with_tax, write CSV.
"""

import csv
from pathlib import Path


def load_csv(path: str) -> list[dict[str, str]]:
    """Read CSV with header; return list of dicts (one per row)."""
    rows = []
    try:
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
    except FileNotFoundError:
        print(f"File not found: {path}")
        return []
    return rows


def filter_rows(
    rows: list[dict[str, str]], region: str
) -> list[dict[str, str]]:
    """Return rows where 'region' equals the given value."""
    return [r for r in rows if r.get("region") == region]


def add_computed_column(
    rows: list[dict[str, str]], cost_key: str = "cost", tax_rate: float = 1.1
) -> list[dict[str, str]]:
    """Add cost_with_tax = cost * tax_rate. Cost may be string; convert to float."""
    for row in rows:
        try:
            cost = float(row.get(cost_key, 0))
        except (ValueError, TypeError):
            cost = 0.0
        row["cost_with_tax"] = round(cost * tax_rate, 2)
    return rows


def write_csv(path: str, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    """Write rows to CSV with the given column order."""
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


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
