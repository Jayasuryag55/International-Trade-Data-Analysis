import re
import pandas as pd
from typing import Optional


CURRENCY_PATTERN_USD = re.compile(r"\bUSD\s*[:]?\s*([\d\.]+)", re.IGNORECASE)
QTY_PATTERN = re.compile(r"QTY[:\s]*([0-9,]+)", re.IGNORECASE)
CAPACITY_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\s*(ML|LITRE|L|CM|MM|INCH|IN)\b",
    re.IGNORECASE,
)
PAREN_MODEL_PATTERN = re.compile(r"\(([A-Z0-9-]{3,})\)")


def _clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    return re.sub(r"\s+", " ", text).strip()


def extract_unit_price_usd(description: str) -> Optional[float]:
    """Extract original unit price in USD, e.g. 'USD 1.5 PER PCS'."""
    desc = _clean_text(description)
    m = CURRENCY_PATTERN_USD.search(desc)
    if not m:
        return None
    try:
        return float(m.group(1))
    except ValueError:
        return None


def extract_embedded_quantity(description: str) -> Optional[float]:
    """Extract embedded QTY: '(QTY: 336000 SETS/USD 0.139 ...)'"""
    desc = _clean_text(description)
    m = QTY_PATTERN.search(desc)
    if not m:
        return None
    qty_str = m.group(1).replace(",", "")
    try:
        return float(qty_str)
    except ValueError:
        return None


def extract_capacity(description: str) -> Optional[str]:
    """Extract capacity/spec like '750ML', '16CM', '10 INCH'."""
    desc = _clean_text(description)
    m = CAPACITY_PATTERN.search(desc)
    if not m:
        return None
    value, unit = m.groups()
    return f"{value}{unit.upper()}"


def extract_model_number(description: str) -> Optional[str]:
    """Heuristic to extract a model number/code."""
    desc = _clean_text(description).upper()

    # Prefer codes in parentheses
    for m in PAREN_MODEL_PATTERN.finditer(desc):
        candidate = m.group(1)
        if any(ch.isdigit() for ch in candidate):
            return candidate

    # Otherwise, first token containing a digit
    for token in desc.split():
        if any(ch.isdigit() for ch in token):
            return token.strip("(),")

    return None


def extract_model_name(description: str, model_number: Optional[str]) -> Optional[str]:
    """Approximate a human‑friendly model name (text without codes/QTY blocks)."""
    desc = _clean_text(description).upper()

    # Cut at QTY if present
    qty_idx = desc.find("QTY")
    if qty_idx != -1:
        desc = desc[:qty_idx]

    # Cut at first '(' (often holds codes)
    paren_idx = desc.find("(")
    if paren_idx != -1:
        desc = desc[:paren_idx]

    # Remove model_number token if we know it
    if model_number:
        desc = desc.replace(model_number.upper(), " ")

    desc = desc.strip(" -/,")
    desc = re.sub(r"\s+", " ", desc)

    if not desc:
        return None
    return desc.title()


def extract_material_type(description: str) -> Optional[str]:
    """Rough material classification based on keywords."""
    desc = _clean_text(description).upper()

    if "STAINLESS STEEL" in desc:
        return "Stainless Steel"
    if "MILD STEEL" in desc:
        return "Mild Steel"
    if "NON STICK" in desc:
        return "Non Stick"
    if "BOROSILICATE" in desc:
        return "Borosilicate Glass"

    if "GLASS" in desc:
        return "Glass"
    if "STEEL" in desc:
        return "Steel"
    if "WOODEN" in desc or "WOOD " in desc:
        return "Wood"
    if "PLASTIC" in desc:
        return "Plastic"

    return None


def parse_goods_description(df: pd.DataFrame,
                            col: str = "Goods Description") -> pd.DataFrame:
    """Parse Goods Description into structured fields."""
    df = df.copy()
    desc_series = df[col].fillna("")

    model_numbers = desc_series.apply(extract_model_number)
    df["model_number"] = model_numbers
    df["model_name"] = [
        extract_model_name(d, mn) for d, mn in zip(desc_series, model_numbers)
    ]
    df["capacity_spec"] = desc_series.apply(extract_capacity)
    df["material_type"] = desc_series.apply(extract_material_type)
    df["embedded_quantity"] = desc_series.apply(extract_embedded_quantity)
    df["unit_price_usd_parsed"] = desc_series.apply(extract_unit_price_usd)

    return df
