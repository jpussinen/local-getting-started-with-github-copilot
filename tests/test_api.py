"""Test cases for the Mergington High School Activities API"""
import pytest


def test_root_redirect(client):
    """Test that root redirects to static index page"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client, reset_activities):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert "Basketball Team" in data
    assert "Swimming Club" in data
    assert "Drama Club" in data
    assert "Art Studio" in data
    assert "Debate Team" in data
    assert "Science Olympiad" in data
    
    # Check structure of one activity
    basketball = data["Basketball Team"]
    assert "description" in basketball
    assert "schedule" in basketball
    assert "max_participants" in basketball
    assert "participants" in basketball
    assert basketball["max_participants"] == 15
    assert len(basketball["participants"]) == 2


def test_signup_for_activity_success(client, reset_activities):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Basketball Team/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Basketball Team" in data["message"]
    
    # Verify the participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "newstudent@mergington.edu" in activities["Basketball Team"]["participants"]


def test_signup_for_nonexistent_activity(client, reset_activities):
    """Test signup for an activity that doesn't exist"""
    response = client.post(
        "/activities/Nonexistent Activity/signup?email=student@mergington.edu"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant(client, reset_activities):
    """Test that a student cannot sign up for the same activity twice"""
    # First signup should succeed
    response1 = client.post(
        "/activities/Basketball Team/signup?email=john@mergington.edu"
    )
    assert response1.status_code == 400
    assert "already signed up" in response1.json()["detail"]


def test_unregister_from_activity_success(client, reset_activities):
    """Test successful unregistration from an activity"""
    response = client.post(
        "/activities/Basketball Team/unregister?email=john@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "john@mergington.edu" in data["message"]
    assert "Basketball Team" in data["message"]
    
    # Verify the participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "john@mergington.edu" not in activities["Basketball Team"]["participants"]


def test_unregister_from_nonexistent_activity(client, reset_activities):
    """Test unregister from an activity that doesn't exist"""
    response = client.post(
        "/activities/Nonexistent Activity/unregister?email=student@mergington.edu"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_non_participant(client, reset_activities):
    """Test that unregistering a non-participant returns an error"""
    response = client.post(
        "/activities/Basketball Team/unregister?email=notsignedup@mergington.edu"
    )
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_signup_and_unregister_flow(client, reset_activities):
    """Test complete flow: signup, verify, unregister, verify"""
    email = "testflow@mergington.edu"
    activity = "Swimming Club"
    
    # Get initial participant count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity]["participants"])
    
    # Sign up
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200
    
    # Verify signup
    after_signup = client.get("/activities")
    assert email in after_signup.json()[activity]["participants"]
    assert len(after_signup.json()[activity]["participants"]) == initial_count + 1
    
    # Unregister
    unregister_response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister_response.status_code == 200
    
    # Verify unregister
    after_unregister = client.get("/activities")
    assert email not in after_unregister.json()[activity]["participants"]
    assert len(after_unregister.json()[activity]["participants"]) == initial_count


def test_activities_data_integrity(client, reset_activities):
    """Test that activity data structure is correct and consistent"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        # Check required fields
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        
        # Check data types
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)
        
        # Check participant count doesn't exceed max
        assert len(activity_data["participants"]) <= activity_data["max_participants"]
