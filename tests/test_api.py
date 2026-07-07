from urllib.parse import quote


def test_get_activities_returns_activity_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_for_activity_adds_participant(client):
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities_response = client.get("/activities")
    assert email in activities_response.json()["Chess Club"]["participants"]


def test_unregister_participant_removes_email_from_activity(client):
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
