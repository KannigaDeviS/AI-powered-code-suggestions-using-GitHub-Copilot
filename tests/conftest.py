"""
Pytest configuration and fixtures for FastAPI tests
"""
import pytest
import sys
from pathlib import Path

# Add src directory to Python path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from app import app, activities


@pytest.fixture
def client():
    """Provide a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before and after each test"""
    initial_state = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team and training",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Tennis lessons and friendly matches",
            "schedule": "Wednesdays and Saturdays, 3:00 PM - 4:30 PM",
            "max_participants": 10,
            "participants": ["james@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theatrical performances and improvisation",
            "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and sculpture techniques",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["mia@mergington.edu"]
        },
        "Debate Team": {
            "description": "Competitive debate and public speaking skills",
            "schedule": "Tuesdays and Thursdays, 4:30 PM - 6:00 PM",
            "max_participants": 16,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments and STEM exploration",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 22,
            "participants": ["ethan@mergington.edu"]
        }
    }
    
    # Clear existing activities and reset
    activities.clear()
    activities.update(initial_state)
    
    yield
    
    # Reset after test
    activities.clear()
    activities.update(initial_state)
