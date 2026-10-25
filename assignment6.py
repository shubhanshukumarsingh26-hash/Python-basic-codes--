#!/usr/bin/env python3
"""A beginner-friendly Pandas data-preprocessing practical.

Accepts .csv, .xls, and .xlsx files. With no input path, it runs on a small
student example dataset. The original input file is never overwritten.

Install dependencies:
    python -m pip install pandas openpyxl xlrd

Examples:
    python preprocess_data.py students.csv
    python preprocess_data.py students.xls --output cleaned.xlsx
    python preprocess_data.py students.csv --drop-columns Remarks --min-marks 50
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("Pandas is required. Install it with: python -m pip install pandas", file=sys.stderr)
    raise SystemExit(2)


def sample_data() -> pd.DataFrame:
    """Return example data containing missing and duplicate values."""
    return pd.DataFrame(
        {
            "Name": ["Asha", "Ravi", "Meera", "Kabir", "Ravi"],
            "Marks": [86, 72, None, 91, 72],
            "City": ["Delhi", "Mumbai", "Delhi", None, "Mumbai"],
            "Remarks": ["Good", "Good", "Needs review", "Excellent", "Good"],
        }
    )


def read_data(path: Path) -> pd.DataFrame:
    """Load one CSV or the first worksheet of an Excel workbook."""
    suffix = path.suffix.lower()
    if suffix == ".csv":
        # utf-8-sig handles common CSVs with or without a UTF-8 BOM.
        try:
            return pd.read_csv(path, encoding="utf-8-sig")
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding="cp1252")
    if suffix in {".xls", ".xlsx"}:
        return pd.read_excel(path)
    raise ValueError("Input must be a .csv, .xls, or .xlsx file.")


def preprocess(data: pd.DataFrame, drop_columns: list[str], min_marks: float | None) -> pd.DataFrame:
    """Clean a DataFrame and optionally filter student marks using loc[]."""
    data = data.copy()
    # Make headers consistent and remove whitespace around text values.
    data.columns = [str(column).strip() for column in data.columns]
    for column in data.select_dtypes(include=["object", "string"]).columns:
        data[column] = data[column].map(lambda value: value.strip() if isinstance(value, str) else value)
        data[column] = data[column].replace(r"^\s*$", pd.NA, regex=True)

    # Remove columns the user identifies as irrelevant, ignoring unknown names.
    existing_drop_columns = [column for column in drop_columns if column in data.columns]
    if existing_drop_columns:
        data = data.drop(columns=existing_drop_columns)

    # Drop rows that are completely empty, then identify and remove duplicates.
    data = data.dropna(how="all")
    duplicate_count = int(data.duplicated().sum())
    print(f"Duplicate rows found: {duplicate_count}")
    data = data.drop_duplicates()

    # Drop fully empty columns. Fill remaining numeric gaps with the median and
    # text gaps with the most frequent value, using fillna().
    data = data.dropna(axis=1, how="all")
    for column in data.columns:
        if not data[column].isna().any():
            continue
        if pd.api.types.is_numeric_dtype(data[column]):
            fill_value = data[column].median()
        else:
            modes = data[column].mode(dropna=True)
            fill_value = modes.iloc[0] if not modes.empty else None
        if fill_value is not None and not pd.isna(fill_value):
            data[column] = data[column].fillna(fill_value)

    # Use loc[] for a meaningful optional filter when a Marks column exists.
    if min_marks is not None:
        if "Marks" not in data.columns:
            raise ValueError("--min-marks requires a column named 'Marks'.")
        data["Marks"] = pd.to_numeric(data["Marks"], errors="coerce")
        data = data.loc[data["Marks"] >= min_marks]

    return data.reset_index(drop=True)


def save_data(data: pd.DataFrame, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    suffix = output.suffix.lower()
    if suffix == ".csv":
        data.to_csv(output, index=False, encoding="utf-8-sig")
    elif suffix == ".xlsx":
        data.to_excel(output, index=False)
    else:
        raise ValueError("Output must be .csv or .xlsx. Excel .xls inputs are saved as .xlsx by default.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preprocess a CSV/Excel dataset with Pandas.")
    parser.add_argument("input", nargs="?", type=Path, help="Input .csv, .xls, or .xlsx file; omit to use sample student data")
    parser.add_argument("-o", "--output", type=Path, help="Output .csv or .xlsx file")
    parser.add_argument("--drop-columns", nargs="*", default=[], metavar="COLUMN", help="Irrelevant columns to remove")
    parser.add_argument("--min-marks", type=float, help="Keep only rows with Marks greater than or equal to this value")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.input:
            if not args.input.is_file():
                raise FileNotFoundError(f"Input file not found: {args.input}")
            original = read_data(args.input)
            default_output = args.input.with_name(
                f"{args.input.stem}_preprocessed{'.csv' if args.input.suffix.lower() == '.csv' else '.xlsx'}"
            )
        else:
            original = sample_data()
            default_output = Path("students_preprocessed.csv")

        print("\nFirst five rows:")
        print(original.head())
        print("\nDataFrame information:")
        original.info()
        print("\nDescriptive statistics:")
        print(original.describe(include="all"))

        cleaned = preprocess(original, args.drop_columns, args.min_marks)
        # Demonstrate selection with loc[] (all rows and available columns).
        selected_columns = [column for column in ["Name", "Marks", "City"] if column in cleaned.columns]
        if selected_columns:
            print("\nSelected data using loc[]:")
            print(cleaned.loc[:, selected_columns])

        output = args.output or default_output
        save_data(cleaned, output)
        print(f"\nPreprocessing complete. Cleaned data saved to: {output}")
        print(f"Rows: {len(original)} → {len(cleaned)}")
        print(f"Missing values remaining: {int(cleaned.isna().sum().sum())}")
        return 0
    except (OSError, ImportError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        if isinstance(exc, ImportError):
            print("Install Excel support with: python -m pip install openpyxl xlrd", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
