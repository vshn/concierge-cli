"""
Tests for concierge-cli's command line interface (CLI)
"""
import os


def test_entrypoint():
    """
    Is entrypoint script installed? (setup.py)
    """
    exit_status = os.system('concierge-cli --help')
    assert exit_status == 0
