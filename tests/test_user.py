
import imp
from app import schemas
from .database import client, session




def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Welcome to my API- Sourav @ HEROKU'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json = {"email": "s2@gmail.com","password":"123" })

    new_user = schemas.UserOut(**res.json())

    print(res.json())
    assert new_user.email =='s2@gmail.com'
    assert res.status_code == 201