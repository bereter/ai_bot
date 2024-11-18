import main
from fastapi.testclient import TestClient

client = TestClient(main.main_app)

def test_create_existing_item():
    response = client.post(
        url="/api/v1/account/signup/",
        headers={"X-Token": "coneofsilence"},
        data={'username': '111111', 'user_email': '111111@kik.ru', 'password': '111111'}
    )
    assert response.status_code == 201
    assert response.json() == {'status': 'The letter was sent by email'}