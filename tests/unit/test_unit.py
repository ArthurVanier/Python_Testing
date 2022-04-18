import server
from tests.mock_const import CLUBS, COMPETITIONS


def test_get_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302


def test_show_summary_valid(client):
    response = client.post("/showSummary", data={"email": "admin@irontemple.com"})
    assert response.status_code == 200


def test_show_summary_wrong_email(client):
    response = client.post("/showSummary", data={"email": "wrongEmail@email.fr"})
    assert response.status_code == 400

    
def test_purchase_places_valid(client, mocker):

    mocker.patch.object(server, 'clubs', CLUBS)
    mocker.patch.object(server, 'competitions', COMPETITIONS)

    response = client.post("/purchasePlaces", data={
        "places": "1",
        "club" : "Simply Lift",
        "competition": "Spring Festival"
    })
    assert response.status_code == 200  


def test_purchase_places_insufficient_points(client, mocker):
    mocker.patch.object(server, 'clubs', CLUBS)
    mocker.patch.object(server, 'competitions', COMPETITIONS)

    response = client.post("/purchasePlaces", data={
        "places": "10",
        "club" : "Iron Temple",
        "competition": "Spring Festival"
    })
    assert response.status_code == 400


def test_purchase_places_insufficient_available_places(client, mocker):
    mocker.patch.object(server, 'clubs', CLUBS)
    mocker.patch.object(server, 'competitions', COMPETITIONS)

    response = client.post("/purchasePlaces", data={
        "places": "10",
        "club" : "Simply Lift",
        "competition": "Fall Classic"
    })
    assert response.status_code == 400 


def test_purchases_more_than_13_places(client, mocker):
    mocker.patch.object(server, 'clubs', CLUBS)
    mocker.patch.object(server, 'competitions', COMPETITIONS)

    response = client.post("/purchasePlaces", data={
        "places": "13",
        "club" : "Simply Lift",
        "competition": "Spring Festival"
    })
    assert response.status_code == 400


def test_purchase_outdated_places(client, mocker):
    mocker.patch.object(server, 'clubs', CLUBS)
    mocker.patch.object(server, 'competitions', COMPETITIONS)

    response = client.post("/purchasePlaces", data={
        "places": "1",
        "club" : "She Lifts",
        "competition": "Fall Classic"
    })
    assert response.status_code == 400


def test_purchase_places_valid_date(client, mocker):
    mocker.patch.object(server, 'clubs', CLUBS)
    mocker.patch.object(server, 'competitions', COMPETITIONS)

    response = client.post("/purchasePlaces", data={
        "places": "0",
        "club" : "Simply Lift",
        "competition": "Spring Festival"
    })
    assert response.status_code == 200


def test_substract_point_used(client, mocker):
    mocker.patch.object(server, 'clubs', CLUBS)
    mocker.patch.object(server, 'competitions', COMPETITIONS)

    response = client.post("/purchasePlaces", data={
        "places": "13",
        "club" : "Simply Lift",
        "competition": "Spring Festival"
    })
    assert response.status_code == 400


def test_substract_too_much_places(client, mocker):
    mocker.patch.object(server, 'clubs', CLUBS)
    mocker.patch.object(server, 'competitions', COMPETITIONS)

    response = client.post("/purchasePlaces", data={
        "places": "13",
        "club" : "Simply Lift",
        "competition": "Spring Festival"
    })
    assert response.status_code == 400


def test_list_of_clubs(client, mocker):
    mocker.patch.object(server, 'clubs', CLUBS)
    mocker.patch.object(server, 'competitions', COMPETITIONS)

    response = client.post("/showSummary", data={"email": "admin@irontemple.com"})
    print(response.data.decode())
    assert response.status_code == 200
    assert  ("Iron Temple : 4") in str(response.data.decode())

def test_book_valid(client, mocker):
    mocker.patch.object(server, 'clubs', CLUBS)
    mocker.patch.object(server, 'competitions', COMPETITIONS)

    response = client.get("/book/Spring Festival/Simply Lift")
    assert response.status_code == 200

def test_book_not_valid(client, mocker):
    mocker.patch.object(server, 'clubs', CLUBS)
    mocker.patch.object(server, 'competitions', COMPETITIONS)

    response = client.get("/book/Spring/Simply Lift")
    assert response.status_code == 400