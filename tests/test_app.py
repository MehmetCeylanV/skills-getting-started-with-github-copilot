import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


BASE_STATE = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = copy.deepcopy(BASE_STATE)
    yield
    app_module.activities = copy.deepcopy(BASE_STATE)


@pytest.fixture()
def client():
    return TestClient(app_module.app)


def test_unregister_participant_removes_email_from_activity(client):
    response = client.delete("/activities/Chess%20Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered michael@mergington.edu from Chess Club"
    }
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]


def test_unregister_participant_returns_not_found_for_unknown_participant(client):
    response = client.delete("/activities/Chess%20Club/participants/unknown@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
