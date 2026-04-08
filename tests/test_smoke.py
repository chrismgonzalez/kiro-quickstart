"""Smoke test to verify test infrastructure is working."""


def test_infrastructure():
    """Verify pytest is working."""
    assert True


def test_imports():
    """Verify we can import the CLI module."""
    from task_tracker import cli
    
    assert cli is not None
    assert hasattr(cli, "cli")
