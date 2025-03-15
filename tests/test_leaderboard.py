from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.core.database import get_db
from app.models.models import Competition, Neuron, Submission
from tests.test_database import override_get_db, TestingSessionLocal

# Override FastAPI's get_db to use test database
app.dependency_overrides[get_db] = override_get_db

# Create a test client
client = TestClient(app)

def submit_results():
    
    # Sample submission data
    test_data = {
        "competition": {"protein": "test_protein", "epoch_number": 3},
        "submissions": [
            {"neuron": {"hotkey": "neuron_1"}, "block_number": 100, "score": 90.5},
            {"neuron": {"hotkey": "neuron_2"}, "block_number": 101, "score": 95.5},
            {"neuron": {"hotkey": "neuron_3"}, "block_number": 101, "score": 95.5},
            {"neuron": {"hotkey": "neuron_1"}, "block_number": 102, "score": 95.5},
            {"neuron": {"hotkey": "neuron_2"}, "block_number": 101, "score": 95.5},
            {"neuron": {"hotkey": "neuron_3"}, "block_number": 102, "score": 95.5}
        ]
    }

    # Send POST request
    response = client.post("/api/submit_results", json=test_data)

    # Assert response
    assert response.status_code == 200
    assert response.json() == {"message": "Submissions successfully recorded"}

def test_leaderboard():
    """Test leaderboard sorting logic."""

    submit_results()

    # Request leaderboard
    response = client.get("/api/leaderboard/?epoch_number=3")

    # Assert response
    assert response.status_code == 200

    expected_result = [
            {"hotkey": "neuron_3", "max_score": 95.5, "block_number": 101},
            {"hotkey": "neuron_2", "max_score": 95.5, "block_number": 101},  # Higher rank due to lower block_number
            {"hotkey": "neuron_1", "max_score": 95.5, "block_number": 102}, # Same score, but higher block number
        ]
    
    assert response.json() == expected_result
