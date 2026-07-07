from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"

    initial_response = client.get("/activities")
    assert initial_response.status_code == 200
    initial_data = initial_response.json()
    assert participant_email in initial_data[activity_name]["participants"]

    response = client.delete(
        f"/activities/{quote(activity_name)}/participants",
        params={"email": participant_email},
    )

    assert response.status_code == 200
    updated_data = client.get("/activities").json()
    assert participant_email not in updated_data[activity_name]["participants"]
