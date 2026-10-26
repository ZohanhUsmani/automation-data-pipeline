import pandas as pd
import pytest

from src.validators import validate, check_range, check_regex
from src.cleaners import normalize_columns, trim_strings


def test_normalize_columns():
    df = pd.DataFrame({" First Name ": [1], "Age(Years)": [2]})
    out = normalize_columns(df)
    assert list(out.columns) == ["first_name", "age(years)"]


def test_trim_strings():
    df = pd.DataFrame({"name": ["  alice  "]})
    out = trim_strings(df)
    assert out["name"].iloc[0] == "alice"


def test_validate_missing_required():
    df = pd.DataFrame({"age": [10]})
    errs = validate(df, {"required": ["name", "age"]})
    assert any("missing required column: name" in e for e in errs)


def test_check_range():
    df = pd.DataFrame({"age": [5, 200]})
    errs = check_range(df, "age", 0, 120)
    assert errs


def test_check_regex():
    df = pd.DataFrame({"email": ["a@b.com", "bad"]})
    errs = check_regex(df, "email", r"^[^@]+@[^@]+\.[^@]+$")
    assert errs