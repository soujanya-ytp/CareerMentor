from uuid import uuid4

from app.models.designation import Designation
from app.models.role import Role
from app.models.user import User
from app.services import auth_service


def test_create_user_accepts_role_and_optional_manager_id(
    client,
    session_factory,
    monkeypatch,
) -> None:
    cognito_sub = uuid4()
    monkeypatch.setattr(auth_service, "create_cognito_user", lambda **_: cognito_sub)
    monkeypatch.setattr(auth_service, "delete_cognito_user", lambda *_: None)

    with session_factory() as session:
        designation = Designation(
            designation_code="MGR",
            designation_name="Manager",
            level_order=1,
        )
        session.add(designation)
        session.commit()
        designation_id = str(designation.id)

    response = client.post(
        "/api/v1/users",
        json={
            "first_name": "pravalika",
            "last_name": "chiti",
            "email": "pra@gmail.com",
            "designation_id": designation_id,
            "password": "changeme123",
            "role": "manager",
        },
    )

    data = response.json()
    assert response.status_code == 201
    assert data == {
        "id": str(cognito_sub),
        "first_name": "pravalika",
        "last_name": "chiti",
        "email": "pra@gmail.com",
        "role_id": data["role_id"],
        "designation_id": designation_id,
        "manager_id": None,
        "is_active": True,
        "role": "manager",
        "name": "pravalika chiti",
    }

    with session_factory() as session:
        user = session.get(User, cognito_sub)
        assert user is not None
        assert user.email == "pra@gmail.com"
        assert user.manager_id is None
        assert user.designation_id == designation.id

        role = session.get(Role, user.role_id)
        assert role is not None
        assert role.role_name == "manager"


def test_create_user_returns_conflict_when_cognito_user_exists(
    client,
    session_factory,
    monkeypatch,
) -> None:
    def raise_duplicate_user(**_):
        raise auth_service.CognitoUserAlreadyExistsError(
            "User with this email already exists in Cognito"
        )

    monkeypatch.setattr(auth_service, "create_cognito_user", raise_duplicate_user)
    monkeypatch.setattr(auth_service, "delete_cognito_user", lambda *_: None)

    with session_factory() as session:
        designation = Designation(
            designation_code="ASC",
            designation_name="Associate",
            level_order=1,
        )
        session.add(designation)
        session.commit()
        designation_id = str(designation.id)

    response = client.post(
        "/api/v1/users",
        json={
            "first_name": "pravalika",
            "last_name": "chiti",
            "email": "pra@gmail.com",
            "designation_id": designation_id,
            "password": "changeme123",
            "role": "manager",
            "manager_id": None,
        },
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists in Cognito"}
