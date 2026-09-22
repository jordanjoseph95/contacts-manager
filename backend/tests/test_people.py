def test_create_person(client):
    group_resp = client.post("/groups", json={"name": "Colleagues"})
    group_id = group_resp.json()["id"]

    response = client.post("/people", json={
        "name": "Alex",
        "phone": "07123456789",
        "email": "alex@example.com",
        "group_id": group_id,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alex"
    assert data["group_id"] == group_id


def test_get_person_not_found(client):
    response = client.get("/people/999999")
    assert response.status_code == 404


def test_update_person(client):
    create = client.post("/people", json={"name": "Sam", "phone": None, "email": None, "group_id": None})
    person_id = create.json()["id"]

    update = client.put(f"/people/{person_id}", json={"name": "Sam Updated", "phone": None, "email": None, "group_id": None})
    assert update.status_code == 200
    assert update.json()["name"] == "Sam Updated"


def test_delete_person(client):
    create = client.post("/people", json={"name": "ToDelete", "phone": None, "email": None, "group_id": None})
    person_id = create.json()["id"]

    delete = client.delete(f"/people/{person_id}")
    assert delete.status_code == 200

    after = client.get(f"/people/{person_id}")
    assert after.status_code == 404