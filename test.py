
import pytest
from pytest_mock import mocker
import json
from server import loadClubs, loadCompetitions

CLUBS=[
    {
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"1"
    },
    {
        "name":"Iron Temple",
        "email": "admin@irontemple.com",
        "points":"4"
    },
    {   "name":"She Lifts",
        "email": "kate@shelifts.co.uk",
        "points":"12"
    }
]

COMPETITIONS=[
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "5"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
]


def test_show_summary(client):
    response = client.post("/showSummary", data={"email": "admin@irontemple.com"})
    assert response.status_code == 200

    response = client.post("/showSummary", data={"email": "wrongEmail@email.fr"})
    assert response.status_code == 400

    response = client.post("/showSummary", data={})
    assert response.status_code == 400

    
def test_purchase_places(client, mocker):
    mocker.patch('server.loadClubs', return_value=CLUBS)
    mocker.patch('server.loadCompetitions', return_value=COMPETITIONS)

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

def test_purchases_more_than_13_places(client, mocker):
    mocker.patch('server.loadClubs', return_value=CLUBS)
    mocker.patch('server.loadCompetitions', return_value=COMPETITIONS)

    response = client.post("/purchasePlaces", data={
        "places": "13",
        "club" : "Simply Lift",
        "competition": "Spring Festival"
    })
    assert response.status_code == 400

def test_purchase_outdated_palces(client, mocker):
    mocker.patch('server.loadClubs', return_value=CLUBS)
    mocker.patch('server.loadCompetitions', return_value=COMPETITIONS)

    response = client.post("/purchasePlaces", data={
        "places": "13",
        "club" : "Simply Lift",
        "competition": "Spring Festival"
    })
    assert response.status_code == 400

    response = client.post("/purchasePlaces", data={
        "places": "1",
        "club" : "She Lifts",
        "competition": "Fall Classic"
    })
    assert response.status_code == 400

    

    