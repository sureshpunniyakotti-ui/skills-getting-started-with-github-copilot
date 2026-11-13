from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(
        {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 2,
                "participants": ["michael@mergington.edu"],
            },
            "Basketball Team": {
                "description": "Practice basketball skills and compete in school games",
                "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
                "max_participants": 1,
                "participants": [],
            },
        }
    )


def test_signup_rejects_duplicate_participants():
    reset_activities()

    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_signup_rejects_full_activity():
    reset_activities()

    response = client.post("/activities/Basketball Team/signup?email=alex@mergington.edu")

    assert response.status_code == 200

    second_response = client.post("/activities/Basketball Team/signup?email=blake@mergington.edu")

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Activity is full"


def test_unregister_removes_participant():
    reset_activities()

    response = client.delete("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]
