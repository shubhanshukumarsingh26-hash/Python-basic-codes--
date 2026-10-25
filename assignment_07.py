#!/usr/bin/env python3
"""Assignment 7: visualize student data with Pandas, Matplotlib, and Seaborn.

Install dependencies:
    python -m pip install pandas matplotlib seaborn

Run with the included example CSV:
    python assignment_07_visualization.py

Or provide another CSV with the same required columns:
    python assignment_07_visualization.py path/to/your_data.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
except ImportError as exc:
    print(
        "A required package is missing. Install the packages with:\n"
        "  python -m pip install pandas matplotlib seaborn\n"
        f"Details: {exc}",
        file=sys.stderr,
    )
    raise SystemExit(2)


REQUIRED_COLUMNS = ["Student", "Maths", "Python", "Attendance", "City"]
NUMERIC_COLUMNS = ["Maths", "Python", "Attendance"]


def load_dataset(csv_path: Path) -> pd.DataFrame:
    """Load and validate the CSV data required by this practical."""
    if not csv_path.is_file():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    data = pd.read_csv(csv_path)
    data.columns = [str(column).strip() for column in data.columns]
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing_columns:
        raise ValueError(
            "The CSV is missing required column(s): " + ", ".join(missing_columns)
        )

    # Convert numeric data and exclude rows that cannot be used in these plots.
    for column in NUMERIC_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    before = len(data)
    data = data.dropna(subset=REQUIRED_COLUMNS).copy()
    removed = before - len(data)
    if removed:
        print(f"Skipped {removed} row(s) with missing or invalid required values.")
    if data.empty:
        raise ValueError("No complete student records are available to plot.")
    return data


def create_plots(data: pd.DataFrame) -> None:
    """Create the four required plots and the optional challenge plots."""
    sns.set_theme(style="whitegrid")

    # 1. Line plot: Python marks by student.
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(data["Student"], data["Python"], marker="o", color="royalblue", label="Python marks")
    ax.set(title="Python Marks of Students", xlabel="Student", ylabel="Python Marks")
    ax.legend()
    ax.tick_params(axis="x", rotation=25)
    fig.tight_layout()

    # 2. Bar plot: compare Maths marks by student.
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(data["Student"], data["Maths"], color="seagreen", label="Maths marks")
    ax.set(title="Maths Marks of Students", xlabel="Student", ylabel="Maths Marks")
    ax.legend()
    ax.tick_params(axis="x", rotation=25)
    fig.tight_layout()

    # 3. Scatter plot: relationship between Maths and Python marks.
    fig, ax = plt.subplots(figsize=(7, 5))
    scatter = ax.scatter(data["Maths"], data["Python"], s=80, color="darkorange", label="Students")
    ax.set(title="Maths vs Python Marks", xlabel="Maths Marks", ylabel="Python Marks")
    ax.legend(handles=[scatter], labels=["Students"])
    fig.tight_layout()

    # 4. Correlation matrix and heatmap.
    correlation = data[NUMERIC_COLUMNS].corr()
    print("\nCorrelation matrix:")
    print(correlation.round(2))
    fig, ax = plt.subplots(figsize=(7, 5.5))
    sns.heatmap(correlation, annot=True, cmap="Blues", vmin=-1, vmax=1, fmt=".2f", ax=ax)
    ax.set_title("Correlation Heatmap")
    fig.tight_layout()

    # Challenge: histogram of Python marks.
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.hist(data["Python"], bins=6, color="mediumpurple", edgecolor="white", label="Python marks")
    ax.set(title="Distribution of Python Marks", xlabel="Python Marks", ylabel="Number of Students")
    ax.legend()
    fig.tight_layout()

    # Challenge: box plot comparing Maths and Python marks.
    fig, ax = plt.subplots(figsize=(7, 5))
    data[NUMERIC_COLUMNS[:2]].plot(kind="box", ax=ax, color="black")
    ax.set(title="Maths and Python Marks", ylabel="Marks")
    fig.tight_layout()

    # Challenge: student counts by city.
    city_counts = data["City"].value_counts()
    fig, ax = plt.subplots(figsize=(7, 5))
    wedges, _ = ax.pie(city_counts.values, startangle=90, autopct="%1.1f%%")
    ax.set_title("Students by City")
    ax.legend(wedges, city_counts.index, title="City", loc="best")
    ax.axis("equal")
    fig.tight_layout()

    # Challenge: display the subject and attendance averages.
    print("\nAverage values:")
    print(data[NUMERIC_COLUMNS].mean().round(2))

    print("\nClose each plot window to continue if your Python environment shows them one at a time.")
    plt.show()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot student data from a CSV file using Matplotlib and Seaborn."
    )
    parser.add_argument(
        "csv_file",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("sample_data_assignment_07.csv"),
        help="CSV path (defaults to the sample CSV beside this program)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        data = load_dataset(args.csv_file)
        print("Dataset:")
        print(data.to_string(index=False))
        create_plots(data)
        return 0
    except (OSError, ValueError, pd.errors.ParserError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
