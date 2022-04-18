import server
from tests.mock_const import CLUBS, COMPETITIONS

def test_valid_successive_purchase_of_places(client, mocker):
    mocker.patch.object(server, 'clubs', CLUBS)
    mocker.patch.object(server, 'competitions', COMPETITIONS)

    response = client.post("/purchasePlaces", data={
        "places": "1",
        "club" : "Simply Lift",
        "competition": "Spring Festival"
    })
    assert response.status_code == 200

    response = client.post("/purchasePlaces", data={
        "places": "1",
        "club" : "Simply Lift",
        "competition": "Spring Festival"
    })
    assert response.status_code == 200

def test_wrong_successive_purchase_of_places(client, mocker):
    mocker.patch.object(server, 'clubs', CLUBS)
    mocker.patch.object(server, 'competitions', COMPETITIONS)

    response = client.post("/purchasePlaces", data={
        "places": "2",
        "club" : "Simply Lift",
        "competition": "Spring Festival"
    })
    assert response.status_code == 200

    response = client.post("/purchasePlaces", data={
        "places": "12",
        "club" : "Simply Lift",
        "competition": "Spring Festival"
    })
    assert response.status_code == 400

def test_update_of_club_point_after_purchase(client, mocker):
    mocker.patch.object(server, 'clubs', CLUBS)
    mocker.patch.object(server, 'competitions', COMPETITIONS)

    response = client.post("/purchasePlaces", data={
        "places": "1",
        "club" : "Simply Lift",
        "competition": "Spring Festival"
    })
    assert response.status_code == 200
    assert CLUBS[0]['points'] == '5'

    response = client.post("/showSummary", data={
        "email" : "john@simplylift.co",
    })
    assert  ("Points available: 5") in str(response.data.decode())