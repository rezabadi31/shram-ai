def test_login_inspector_success(client):
    response = client.post(
        "/api/v1/auth/login/json",
        json={"email": "inspector@shram.gov.in", "password": "Inspector@123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "inspector"
    assert data["name"] == "S. K. Sharma"


def test_login_employer_success(client):
    response = client.post(
        "/api/v1/auth/login/json",
        json={"email": "employer@abcindustries.com", "password": "Employer@123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "employer"
    assert data["name"] == "Rajiv Mehra"


def test_login_invalid_password(client):
    response = client.post(
        "/api/v1/auth/login/json",
        json={"email": "inspector@shram.gov.in", "password": "WrongPassword!"},
    )
    assert response.status_code == 401


def test_get_current_user_profile(client):
    # Login first
    login_res = client.post(
        "/api/v1/auth/login/json",
        json={"email": "inspector@shram.gov.in", "password": "Inspector@123"},
    )
    token = login_res.json()["access_token"]

    # Access protected /me endpoint
    me_res = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_res.status_code == 200
    profile = me_res.json()
    assert profile["email"] == "inspector@shram.gov.in"
    assert profile["role"] == "inspector"
    assert profile["designation"] == "Assistant Labour Commissioner (Central)"


def test_unauthenticated_profile_access(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_employer_forbidden_from_inspector_endpoints(client):
    """Employer token must receive 403 when calling inspector-only endpoints."""
    login_res = client.post(
        "/api/v1/auth/login/json",
        json={"email": "employer@abcindustries.com", "password": "Employer@123"},
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Calling establishments list (inspector queue)
    res_queue = client.get("/api/v1/establishments", headers=headers)
    assert res_queue.status_code == 403
    assert "Your account does not have Inspector permissions" in res_queue.json()["detail"]

    # Calling inspection start
    res_start = client.post(
        "/api/v1/inspection/start",
        params={"establishment_id": "EST-001", "establishment_name": "ABC"},
        headers=headers,
    )
    assert res_start.status_code == 403
    assert "Your account does not have Inspector permissions" in res_start.json()["detail"]


def test_inspector_forbidden_from_employer_endpoints(client):
    """Inspector token must receive 403 when calling employer-only endpoints."""
    login_res = client.post(
        "/api/v1/auth/login/json",
        json={"email": "inspector@shram.gov.in", "password": "Inspector@123"},
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/v1/employer/EST-001/profile", headers=headers)
    assert res.status_code == 403
    assert "exclusively for registered Employers" in res.json()["detail"]


def test_employer_data_isolation_between_establishments(client):
    """Employer A (EST-001) must NOT be able to request EST-002 data."""
    login_res = client.post(
        "/api/v1/auth/login/json",
        json={"email": "employer@abcindustries.com", "password": "Employer@123"},
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Accessing own establishment EST-001 should succeed
    res_own = client.get("/api/v1/employer/EST-001/profile", headers=headers)
    assert res_own.status_code == 200

    # Accessing other establishment EST-002 should return 403
    res_other = client.get("/api/v1/employer/EST-002/profile", headers=headers)
    assert res_other.status_code == 403
    assert "Employers may only access their own establishment records" in res_other.json()["detail"]

    # Accessing other establishment dossier on /establishments/EST-002 should also return 403
    res_dossier = client.get("/api/v1/establishments/EST-002", headers=headers)
    assert res_dossier.status_code == 403
    assert "Employers may only access their own establishment records" in res_dossier.json()["detail"]

