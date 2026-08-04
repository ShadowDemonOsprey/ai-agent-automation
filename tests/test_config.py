from app.core.config import settings


def test_default_environment():
    """
    Verify that the application loads
    with a valid default environment.
    """

    assert settings.app_env in [
        "development",
        "production"
    ]


def test_app_name_exists():
    """
    Verify that application name
    is loaded correctly.
    """

    assert settings.app_name == "AI Agent Automation Platform"

