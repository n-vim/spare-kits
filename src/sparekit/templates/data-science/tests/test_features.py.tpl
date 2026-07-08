import pandas as pd

from {{ package_name }}.features import add_ratio_feature


def test_add_ratio_feature() -> None:
    df = pd.DataFrame({"a": [10, 20], "b": [2, 4]})
    result = add_ratio_feature(df, "a", "b", "ratio")
    assert result["ratio"].tolist() == [5.0, 5.0]
