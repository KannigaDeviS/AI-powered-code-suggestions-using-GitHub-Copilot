"""
Comprehensive tests for FastAPI application
"""
import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client):
        """Test that all activities are returned"""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data
    
    def test_get_activities_structure(self, client):
        """Test that activity structure is correct"""
        response = client.get("/activities")
        data = response.json()
        
        activity = data["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)
    
    def test_get_activities_participants_count(self, client):
        """Test that participants are correctly counted"""
        response = client.get("/activities")
        data = response.json()
        
        chess_club = data["Chess Club"]
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_successful(self, client):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]
    
    def test_signup_adds_participant(self, client):
        """Test that signup actually adds the participant"""
        # Signup
        email = "newstudent@mergington.edu"
        client.post(
            "/activities/Chess%20Club/signup",
            params={"email": email}
        )
        
        # Verify participant was added
        response = client.get("/activities")
        data = response.json()
        assert email in data["Chess Club"]["participants"]
    
    def test_signup_nonexistent_activity(self, client):
        """Test signup for non-existent activity returns 404"""
        response = client.post(
            "/activities/NonExistent%20Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]
    
    def test_signup_duplicate_participant(self, client):
        """Test signup for same participant twice returns 400"""
        email = "michael@mergington.edu"  # Already in Chess Club
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": email}
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]
    
    def test_signup_multiple_activities(self, client):
        """Test that a student can signup for multiple activities"""
        email = "multiactivity@mergington.edu"
        
        # Signup for Chess Club
        response1 = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Signup for Programming Class
        response2 = client.post(
            "/activities/Programming%20Class/signup",
            params={"email": email}
        )
        assert response2.status_code == 200
        
        # Verify in both activities
        response = client.get("/activities")
        data = response.json()
        assert email in data["Chess Club"]["participants"]
        assert email in data["Programming Class"]["participants"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_successful(self, client):
        """Test successful unregistration from an activity"""
        email = "michael@mergington.edu"
        response = client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert "Chess Club" in data["message"]
    
    def test_unregister_removes_participant(self, client):
        """Test that unregister actually removes the participant"""
        email = "michael@mergington.edu"
        
        # Verify participant is there
        response = client.get("/activities")
        assert email in response.json()["Chess Club"]["participants"]
        
        # Unregister
        client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": email}
        )
        
        # Verify participant was removed
        response = client.get("/activities")
        assert email not in response.json()["Chess Club"]["participants"]
    
    def test_unregister_nonexistent_activity(self, client):
        """Test unregister from non-existent activity returns 404"""
        response = client.delete(
            "/activities/NonExistent%20Activity/unregister",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]
    
    def test_unregister_not_registered_participant(self, client):
        """Test unregister for non-registered participant returns 400"""
        response = client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": "notstudent@mergington.edu"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "not registered" in data["detail"]
    
    def test_unregister_then_signup_again(self, client):
        """Test that participant can unregister and signup again"""
        email = "michael@mergington.edu"
        
        # Unregister
        response1 = client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Signup again
        response2 = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": email}
        )
        assert response2.status_code == 200
        
        # Verify in activity
        response = client.get("/activities")
        assert email in response.json()["Chess Club"]["participants"]


class TestIntegration:
    """Integration tests combining multiple operations"""
    
    def test_full_workflow(self, client):
        """Test complete workflow: signup, check, unregister, check"""
        email = "workflow@mergington.edu"
        activity = "Chess%20Club"
        
        # Initially not in activity
        response = client.get("/activities")
        assert email not in response.json()["Chess Club"]["participants"]
        
        # Signup
        response = client.post(f"/activities/{activity}/signup", params={"email": email})
        assert response.status_code == 200
        
        # Verify in activity
        response = client.get("/activities")
        assert email in response.json()["Chess Club"]["participants"]
        
        # Unregister
        response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
        assert response.status_code == 200
        
        # Verify not in activity
        response = client.get("/activities")
        assert email not in response.json()["Chess Club"]["participants"]
    
    def test_multiple_students_same_activity(self, client):
        """Test multiple students in same activity"""
        emails = ["student1@test.edu", "student2@test.edu", "student3@test.edu"]
        
        # Signup multiple students
        for email in emails:
            response = client.post(
                "/activities/Programming%20Class/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify all are in activity
        response = client.get("/activities")
        prog_class = response.json()["Programming Class"]
        for email in emails:
            assert email in prog_class["participants"]
        
        # Unregister middle student
        client.delete(
            "/activities/Programming%20Class/unregister",
            params={"email": emails[1]}
        )
        
        # Verify correct removal
        response = client.get("/activities")
        prog_class = response.json()["Programming Class"]
        assert emails[0] in prog_class["participants"]
        assert emails[1] not in prog_class["participants"]
        assert emails[2] in prog_class["participants"]
