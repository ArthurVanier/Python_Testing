from .server import app as app_server
import pytest

@pytest.fixture
def client():
    with app_server.test_client() as client:
        yield client
