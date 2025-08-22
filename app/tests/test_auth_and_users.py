from http import HTTPStatus

def register(client, name, email, password):
    return client.post("/users", json={"name": name, "email": email, "password": password})

def login(client, email, password):
    return client.post("/login", data={"username": email, "password": password})

def auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def test_register_and_login_and_me(client):
    # Register
    r = register(client, "Alice", "alice@example.com", "Str0ng!Pass")
    assert r.status_code == HTTPStatus.CREATED, r.text
    user = r.json()
    assert "password_hash" not in user
    assert user["email"] == "alice@example.com"

    # Duplicate
    r2 = register(client, "Alice2", "alice@example.com", "Str0ng!Pass")
    assert r2.status_code == HTTPStatus.CONFLICT

    # Login
    resp = login(client, "alice@example.com", "Str0ng!Pass")
    assert resp.status_code == HTTPStatus.OK, resp.text
    token = resp.json()["access_token"]

    # Me
    me = client.get("/me", headers=auth_header(token))
    assert me.status_code == HTTPStatus.OK
    assert me.json()["email"] == "alice@example.com"

def test_rbac_user_fetch_and_list(client):
    # create normal user
    u = register(client, "Bob", "bob@example.com", "BobStrong1!").json()
    # create admin
    admin = register(client, "Admin", "admin@example.com", "AdminStrong1!").json()

    # make admin actually admin via direct DB override route not provided;
    # Instead, login then attempt list -> should be forbidden (since role=user).
    t_user = login(client, "bob@example.com", "BobStrong1!").json()["access_token"]
    t_admin = login(client, "admin@example.com", "AdminStrong1!").json()["access_token"]

    # Normal user cannot get other user
    r = client.get(f"/users/{admin['id']}", headers=auth_header(t_user))
    assert r.status_code in (HTTPStatus.FORBIDDEN, HTTPStatus.NOT_FOUND)

    # Normal user can get themselves
    r2 = client.get(f"/users/{u['id']}", headers=auth_header(t_user))
    assert r2.status_code == HTTPStatus.OK

    # Listing users requires admin -> expect forbidden
    r3 = client.get("/users", headers=auth_header(t_user))
    assert r3.status_code == HTTPStatus.FORBIDDEN

    # Since API has no admin elevate endpoint in core requirements,
    # we stop here. Seed script covers real admin creation.
