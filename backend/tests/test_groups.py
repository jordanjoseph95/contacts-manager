def test_create_group(client):
    response = client.post("/groups", json={"name": "Friens"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Friends"
    assert "id" in data


def test_list_groups(client):
    client.post("/groups", json={"name": "Family"})
    response = client.get("/groups")
    assert response.status_code == 200
    names = [g["name"] for g in response.json()]
    assert "Family" in names