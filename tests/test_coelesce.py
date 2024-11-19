from unittest.mock import patch

from fastapi.testclient import TestClient

from adapters.utils import get_mode_or_avg
from app.main import app, get_default_config
from tests.utils import async_side_effect_1, async_side_effect_2

client = TestClient(app)


@patch("httpx.AsyncClient.get")
def test_aggregate_endpoint_config_1(mock_get):
    mock_get.side_effect = async_side_effect_1

    def get_custom_config_for_test():
        return None

    app.dependency_overrides[get_default_config] = get_custom_config_for_test

    response = client.get("/insurance-info?member_id=1")

    # Reset the dependency overrides after the test, otherwise values will persist
    app.dependency_overrides.clear()

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "oop_max": 10000,
        "remaining_oop_max": 9000,
        "copay": 1000,
    }


@patch("httpx.AsyncClient.get")
def test_aggregate_endpoint_config_2(mock_get):
    mock_get.side_effect = async_side_effect_1

    def get_custom_config_for_test():
        return {"oop_max": "max", "remaining_oop_max": "max", "copay": "max"}

    app.dependency_overrides[get_default_config] = get_custom_config_for_test

    response = client.get("/insurance-info?member_id=1")

    # Reset the dependency overrides after the test, otherwise values will persist
    app.dependency_overrides.clear()

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "copay": 50000,
        "oop_max": 20000,
        "remaining_oop_max": 9000,
    }


@patch("httpx.AsyncClient.get")
def test_aggregate_endpoint_config_3(mock_get):
    mock_get.side_effect = async_side_effect_1

    def get_custom_config_for_test():
        return {"oop_max": "avg", "remaining_oop_max": "max", "copay": "max"}

    app.dependency_overrides[get_default_config] = get_custom_config_for_test

    response = client.get("/insurance-info?member_id=1")

    # Reset the dependency overrides after the test, otherwise values will persist
    app.dependency_overrides.clear()

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "copay": 50000,
        "oop_max": 13333,
        "remaining_oop_max": 9000,
    }


@patch("httpx.AsyncClient.get")
def test_aggregate_endpoint_config_4(mock_get):
    mock_get.side_effect = async_side_effect_1

    def get_custom_config_for_test():
        return {
            "oop_max": "avg",
            "remaining_oop_max": "max",
            "copay": lambda amounts: sum(amounts) // len(amounts),
        }

    app.dependency_overrides[get_default_config] = get_custom_config_for_test

    response = client.get("/insurance-info?member_id=1")

    # Reset the dependency overrides after the test, otherwise values will persist
    app.dependency_overrides.clear()

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "copay": 17333,
        "oop_max": 13333,
        "remaining_oop_max": 9000,
    }


@patch("httpx.AsyncClient.get")
def test_aggregate_endpoint_config_5(mock_get):
    mock_get.side_effect = async_side_effect_2

    def get_custom_config_for_test():
        return {
            "oop_max": "avg",
            "remaining_oop_max": "max",
            "copay": lambda amounts: get_mode_or_avg(amounts),
        }

    app.dependency_overrides[get_default_config] = get_custom_config_for_test

    response = client.get("/insurance-info?member_id=1")

    # Reset the dependency overrides after the test, otherwise values will persist
    app.dependency_overrides.clear()

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "copay": 11000,
        "oop_max": 13333,
        "remaining_oop_max": 9000,
    }
