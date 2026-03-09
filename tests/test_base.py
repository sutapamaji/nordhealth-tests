import pytest

@pytest.mark.usefixtures("app_page")
class TestBase:
    """
    Base test class to be inherited by all test scripts.
    It automatically requests the shared `app_page` fixture.
    """
    pass
