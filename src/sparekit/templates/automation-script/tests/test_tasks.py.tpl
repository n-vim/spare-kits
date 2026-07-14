from {{ package_name }}.tasks import run_cleanup_task


def test_run_cleanup_task() -> None:
    result = run_cleanup_task(dry_run=True)
    assert result.success is True
    assert result.name == "cleanup"
