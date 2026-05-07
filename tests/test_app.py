import copy
import pytest
from fastapi.testclient import TestClient
from src import app as app_module

client = TestClient(app_module.app)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset in-memory activities state around each test."""
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))


def test_signup_adds_participant():
    activity = "Chess Club"
    email = "test@student.edu"

    # Ensure clean start
    if email in app_module.activities[activity]["participants"]:
        app_module.activities[activity]["participants"].remove(email)

    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert email in app_module.activities[activity]["participants"]


def test_signup_duplicate_returns_400():
    activity = "Chess Club"
    email = "duplicate@student.edu"

    # Ensure email is present
    if email not in app_module.activities[activity]["participants"]:
        app_module.activities[activity]["participants"].append(email)

    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 400


def test_delete_removes_participant():
    activity = "Programming Class"
    email = "remove@student.edu"

    if email not in app_module.activities[activity]["participants"]:
        app_module.activities[activity]["participants"].append(email)

    res = client.delete(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert email not in app_module.activities[activity]["participants"]


def test_delete_nonexistent_returns_404():
    activity = "Programming Class"
    email = "nonexistent@student.edu"

    if email in app_module.activities[activity]["participants"]:
        app_module.activities[activity]["participants"].remove(email)

    res = client.delete(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 404
