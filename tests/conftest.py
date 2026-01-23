"""Pytest configuration and fixtures"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store original state
    original_activities = {
        "Basketball Team": {
            "description": "Join the school basketball team and compete in league games",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["john@mergington.edu", "michael@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Improve your swimming techniques and participate in swim meets",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["olivia@mergington.edu", "emma@mergington.edu"]
        },
        "Drama Club": {
            "description": "Participate in theater productions and develop acting skills",
            "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["sophia@mergington.edu", "emily@mergington.edu"]
        },
        "Art Studio": {
            "description": "Express creativity through painting, drawing, and sculpture",
            "schedule": "Fridays, 3:00 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["daniel@mergington.edu", "ava@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop critical thinking and public speaking through competitive debates",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["michael@mergington.edu", "sophia@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Compete in science competitions and conduct experiments",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "john@mergington.edu"]
        }
    }
    
    # Reset activities to original state
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Clean up after test
    activities.clear()
    activities.update(original_activities)
