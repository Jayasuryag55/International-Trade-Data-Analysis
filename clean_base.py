import pandas as pd
from pathlib import Path
from typing import Optional

from src.parsing.parse_goods_description import parse_goods_description


ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = ROOT / "data" / "raw" / "Siddharth_Associates_sample data 2.xlsx"


def normalize_unit(unit: Optional[str]) -> Optional[str]:
    """Standardize unit variants into a few canonical labels."""
    if not isinstance(unit, str):
        return None
    u = unit.strip().upper()

    mapping = {
        "PCS": "PCS",
        "PC": "PCS",
        "NOS": "PCS",
        "PIECE": "PCS",
        "PIECES": "PCS",
        "SET": "SET",
        "SETS": "SET",
        "KG": "KG",
        "KGS": "KG",
        "KILOGRAM": "KG",
        "MT": "MT",
        "METRIC TON": "MT",
    }

    return mapping.get(u, u)


def load_raw_data(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    return pd.read_excel(path)


def clean_dates(df: pd.DataFrame,
                date_col: str = "Date of Shipment") -> pd.DataFrame:
    """Convert Date of Shipment to datetime and derive year/month/quarter."""
    df = df.copy()
    df["date_of_shipment"] = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)
    df["year"] = df["date_of_shipment"].dt.year
    df["month"] = df["date_of_shipment"].dt.month
    df["quarter"] = df["date_of_shipment"].dt.quarter
    return df


def handle_basic_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows missing critical numeric columns."""
    df = df.copy()
    df = df.dropna(subset=["Total Value (INR)", "Duty Paid (INR)", "Quantity"])
    return df


def apply_unit_standardization(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["unit_standardized"] = df["Unit"].apply(normalize_unit)
    return df


def run_base_cleaning() -> pd.DataFrame:
    df = load_raw_data()
    df = clean_dates(df)
    df = handle_basic_missing(df)
    df = parse_goods_description(df, col="Goods Description")
    df = apply_unit_standardization(df)
    return df


if __name__ == "__main__":
    df_clean = run_base_cleaning()
    out_path = ROOT / "data" / "processed" / "trade_cleaned_step1.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(out_path, index=False)
    print(f"Base cleaned data saved to: {out_path}")
