
from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlalchemy import select

from fast_zero.app import app
from fast_zero.models import User

DEFAULT_TEST_USERS_COUNT = 2


def test_root_deve_retornar_ok_e_ola_mundo():

    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_exercicio_ola_mundo_em_html():
    client = TestClient(app)

    response = client.get('/exercicio-html')

    assert response.status_code == HTTPStatus.OK
    assert '<h1>Olá Mundo!</h1>' in response.text


def test_create_user(session):
    new_user = User(username='alice', password='secret', email='teste@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'


def test_read_users(session):
    users = [
        User(username='alice', password='secret', email='alice@example.com'),
        User(username='bob', password='secret', email='bob@example.com')
    ]
    session.add_all(users)
    session.commit()

    query = select(User)
    result = session.scalars(query).all()

    assert len(result) == DEFAULT_TEST_USERS_COUNT
    assert result[0].username == 'alice'
    assert result[1].username == 'bob'


def test_update_user(session):
    user = User(username='alice', password='secret', email='alice@example.com')
    session.add(user)
    session.commit()

    user.username = 'alice_updated'
    user.email = 'new_email@example.com'
    session.commit()

    updated_user = session.scalar(select(User).where(User.id == user.id))

    assert updated_user.username == 'alice_updated'
    assert updated_user.email == 'new_email@example.com'


def test_delete_user(session):
    user = User(username='alice', password='secret', email='alice@example.com')
    session.add(user)
    session.commit()

    user_id = user.id

    session.delete(user)
    session.commit()

    deleted_user = session.scalar(select(User).where(User.id == user_id))

    assert deleted_user is None
