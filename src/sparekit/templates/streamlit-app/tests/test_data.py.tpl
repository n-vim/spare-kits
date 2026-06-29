from {{ package_name }}.data import sample_metrics


def test_sample_metrics() -> None:
    assert sample_metrics()["Users"] > 0
