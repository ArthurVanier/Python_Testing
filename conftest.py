from server import app as app_server
import pytest

@pytest.fixture
def app():
    return app_server