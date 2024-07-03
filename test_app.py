import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "OpenClassrooms".encode('utf-8') in response.data  # Vérifier si le texte est présent dans la réponse

def test_valid_id(client):
    response = client.post('/predict', data={'client_id': 100002})
    assert response.status_code == 200
    data = response.get_json()
    assert 'prediction' in data  # Vérifier si 'prediction' est dans la réponse

def test_invalid_id(client):
    response = client.post('/predict', data={'client_id': 0}) 
    assert response.status_code == 200
    data = response.get_json()
    assert 'erreur' in data  # Vérifier si 'erreur' est dans la réponse
    assert 'prediction' not in data  # Vérifier que 'prediction' n'est pas dans la réponse

if __name__ == '__main__':
    pytest.main()