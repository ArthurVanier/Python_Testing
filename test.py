
import pytest

def test_show_summary(client):
    response = client.post("/showSummary", data={"email": "admin@irontemple.com"})
    assert response.status_code == 200

    response = client.post("/showSummary", data={"email": "wrongEmail@email.fr"})
    assert response.status_code == 400

    response = client.post("/showSummary", data={})
    assert response.status_code == 400

    
def test_purchase_places(client):
    response = client.post("/purchasePlaces", data={
        "places": "10",
        "club" : "Simply Lift",
        "competition": "Spring Festival"
    })
    assert response.status_code == 200
    
    response = client.post("/purchasePlaces", data={
        "places": "10",
        "club" : "Simply Lift",
        "competition": "Spring Festival"
    })
    assert response.status_code == 400

    response = client.post("/purchasePlaces", data={
        "places": "50",
        "club" : "Simply Lift",
        "competition": "Spring Festival"

    })
    assert response.status_code == 400    