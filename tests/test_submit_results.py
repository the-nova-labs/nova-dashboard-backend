from fastapi.testclient import TestClient
from app.core.database import get_db
from app.main import app
from app.models.models import Competition, Neuron, Submission
from tests.test_database import override_get_db, TestingSessionLocal


# Override FastAPI's get_db to use test database
app.dependency_overrides[get_db] = override_get_db

# Create a test client
client = TestClient(app)

def test_submit_results():
    """Test submitting results with competition and neuron creation."""

    # Sample submission data
    test_data = {
        "competition": {
            "target_protein": "test_protdsdsein", 
            "anti_target_protein": "test_pdfsdrotein",
            "epoch_number": 23,
        },
        "submissions": [
            {"neuron": {"hotkey": "neuron_1"}, "block_number": 100, "score": 95.5, "molecule": "test_molecule2"},
            {"neuron": {"hotkey": "neuron_2"}, "block_number": 101, "score": 190.0, "molecule": "test_mdolecule2"},
            {"neuron": {"hotkey": "neuron_3"}, "block_number": 102, "score": 85.0, "molecule": "test_molecule3"}
        ]
    }

    # Send POST request
    response = client.post("/api/submit_results", json=test_data)

    # Assert response
    assert response.status_code == 200
    assert response.json() == {"success": True}

