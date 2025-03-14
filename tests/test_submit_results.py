from fastapi.testclient import TestClient
from app.core.database import get_db
from app.main import app
from app.models.models import Competition, Neuron, Submission
from tests.test_database import override_get_db, TestingSessionLocal


# Override FastAPI's get_db to use test database
app.dependency_overrides[get_db] = override_get_db

# Create a test client
client = TestClient(app)

# def test_submit_results():
#     """Test submitting results with competition and neuron creation."""

#     # Sample submission data
#     test_data = {
#         "competition": {"protein": "test_protein", "epoch_number": 2},
#         "submissions": [
#             {"neuron": {"hotkey": "neuron_1"}, "block_number": 100, "score": 95.5},
#             {"neuron": {"hotkey": "neuron_2"}, "block_number": 101, "score": 90.0},
#             {"neuron": {"hotkey": "neuron_3"}, "block_number": 102, "score": 85.0}
#         ]
#     }

#     # Send POST request
#     response = client.post("/api/submit_results", json=test_data)

#     # Assert response
#     assert response.status_code == 200
#     assert response.json() == {"message": "Submissions successfully recorded"}

#     # Verify data was inserted into the database
#     with TestingSessionLocal() as db:
#         assert db.query(Competition).count() == 2  # Competition was created
#         assert db.query(Neuron).count() == 3  # Both neurons were created
#         assert db.query(Submission).count() == 20  # Two submissions were recorded
