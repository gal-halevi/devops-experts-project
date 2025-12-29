def test_healthz_ok(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_readyz_ok_when_can_read_and_write(client):
    resp = client.get("/readyz")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["ready"] is True


def test_root_increments_counter(client):
    r1 = client.get("/")
    assert r1.status_code == 200
    c1 = r1.get_json()["counter"]

    r2 = client.get("/")
    assert r2.status_code == 200
    c2 = r2.get_json()["counter"]

    assert c2 == c1 + 1


def test_count_does_not_increment(client):
    # increment once
    client.get("/")
    r = client.get("/count")
    assert r.status_code == 200
    c_before = r.get_json()["counter"]

    # count again should be same
    r2 = client.get("/count")
    assert r2.status_code == 200
    c_after = r2.get_json()["counter"]

    assert c_after == c_before


def test_inc_post_increments(client):
    r1 = client.post("/inc")
    assert r1.status_code == 200
    c1 = r1.get_json()["counter"]

    r2 = client.post("/inc")
    assert r2.status_code == 200
    c2 = r2.get_json()["counter"]

    assert c2 == c1 + 1


def test_invalid_counter_file_content_treated_as_zero(app_module, client, tmp_path):
    # write invalid content directly to the counter file
    counter_path = tmp_path / "counter.txt"
    counter_path.write_text("not-a-number")

    # /count should treat invalid as 0
    r = client.get("/count")
    assert r.status_code == 200
    assert r.get_json()["counter"] == 0


def test_admin_reset_requires_token(client):
    r = client.post("/admin/reset")
    assert r.status_code == 401
    assert r.get_json()["error"] == "unauthorized"


def test_admin_reset_success(app_module, client, monkeypatch):
    # set token in env (read at request time, so no reload needed)
    monkeypatch.setenv("ADMIN_TOKEN", "secret")

    # increment a few times
    client.get("/")
    client.get("/")
    assert client.get("/count").get_json()["counter"] >= 2

    # reset with correct header
    r = client.post("/admin/reset", headers={"X-Admin-Token": "secret"})
    assert r.status_code == 200
    assert r.get_json()["message"] == "counter reset"

    # verify reset
    assert client.get("/count").get_json()["counter"] == 0


def test_readyz_returns_503_when_write_fails(app_module, client, monkeypatch):
    # Simulate failure without messing with filesystem permissions
    def boom(_value: int) -> None:
        raise PermissionError("nope")

    monkeypatch.setattr(app_module, "write_counter", boom)
    r = client.get("/readyz")
    assert r.status_code == 503
    body = r.get_json()
    assert body["ready"] is False
    assert "nope" in body["error"]