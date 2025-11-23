import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INTERMEDIATE_PATH = ROOT / "data" / "processed" / "trade_cleaned_step1.csv"
FINAL_PATH = ROOT / "data" / "processed" / "trade_cleaned.csv"


def compute_grand_total(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Grand Total (INR)"] = df["Total Value (INR)"] + df["Duty Paid (INR)"]
    return df


def compute_landed_cost_per_unit(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    def _landed(row):
        qty = row.get("Quantity")
        if qty is None or qty == 0:
            return None
        return row["Grand Total (INR)"] / qty

    df["Landed Cost Per Unit (INR)"] = df.apply(_landed, axis=1)
    return df


def assign_category(row: pd.Series) -> str:
    desc = (str(row.get("Goods Description", "")) + " " +
            str(row.get("HSN Description", ""))).upper()

    if "BOTTLE" in desc:
        return "Bottle"
    if any(x in desc for x in ["FRY PAN", "SAUCE PAN", "TAVA", "TAWA", "KADAI"]):
        return "Cookware"
    if "SCRUB" in desc:
        return "Cleaning"
    if "CLOTH" in desc and ("STAND" in desc or "DRYING" in desc):
        return "Laundry"
    if any(x in desc for x in ["HANGER", "HOOK"]):
        return "Hanger/Hook"
    if any(x in desc for x in ["CUTLERY", "SPOON", "FORK", "TEA STRAINER"]):
        return "Tableware"
    if "LUNCH BOX" in desc:
        return "Lunch Box"

    if "GLASS" in desc:
        return "Glass"
    if "WOOD" in desc or "WOODEN" in desc:
        return "Wooden"
    if "STEEL" in desc or "SS " in desc:
        return "Steel"
    if "PLASTIC" in desc:
        return "Plastic"

    hsn = str(row.get("HSN Code", ""))
    if hsn.startswith("73"):
        return "Steel Articles"

    return "Others"


def assign_sub_category(row: pd.Series) -> str:
    desc = (str(row.get("Goods Description", "")) + " " +
            str(row.get("HSN Description", ""))).upper()
    cat = row.get("Category", "Others")

    if cat == "Bottle":
        if "SPORTS" in desc:
            return "Sports Bottle"
        if "COLA" in desc:
            return "Cola Bottle"
        return "Generic Bottle"

    if cat == "Cookware":
        if "FRY PAN" in desc:
            return "Fry Pan"
        if "SAUCE PAN" in desc:
            return "Sauce Pan"
        if "KADAI" in desc:
            return "Kadai"
        return "Other Cookware"

    if cat == "Cleaning":
        if "SCRUBBER" in desc or "SCRUB PAD" in desc:
            return "Scrubber"
        return "Cleaning Tool"

    if cat == "Tableware":
        if "TEA STRAINER" in desc:
            return "Tea Strainer"
        if "CUTLERY" in desc:
            return "Cutlery Holder"
        if "SPOON" in desc or "FORK" in desc:
            return "Spoon/Fork"
        return "Other Tableware"

    if cat == "Lunch Box":
        return "Lunch Box"

    if cat == "Hanger/Hook":
        if "HANGER" in desc:
            return "Hanger"
        if "HOOK" in desc:
            return "Hook"
        return "Hanger/Hook Other"

    if "BOROSILICATE" in desc:
        return "Borosilicate"
    if "OPAL" in desc or "OPALWARE" in desc:
        return "Opalware"

    return "Others"


def add_categories(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Category"] = df.apply(assign_category, axis=1)
    df["Sub-Category"] = df.apply(assign_sub_category, axis=1)
    return df


def add_duty_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Duty %"] = df["Duty Paid (INR)"] / df["Total Value (INR)"]
    duty_mean = df["Duty %"].mean()
    duty_std = df["Duty %"].std()
    df["Duty_ZScore"] = (df["Duty %"] - duty_mean) / duty_std
    df["Duty_Anomaly_Flag"] = df["Duty_ZScore"].abs() > 2
    return df


def run_feature_engineering() -> pd.DataFrame:
    df = pd.read_csv(INTERMEDIATE_PATH)
    df = compute_grand_total(df)
    df = compute_landed_cost_per_unit(df)
    df = add_categories(df)
    df = add_duty_anomalies(df)
    return df


if __name__ == "__main__":
    df_features = run_feature_engineering()
    FINAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_features.to_csv(FINAL_PATH, index=False)
    print(f"Feature engineered data saved to: {FINAL_PATH}")
