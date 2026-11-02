import pytest


def payload(equiptment_id = "34", borrower_name = "Sean Keogh", loan_days ="8", purpose ="To help me get my work done"):
    return{"equiptment_id": equiptment_id, "borrower_name":borrower_name, "loan days": loan_days, "purpose": purpose}

def test_create_loan_returns_201(client):
    response = client.post("/api/loans",json = payload())

    assert response.status_code == 201
    data =response.json()
    assert data["id"] == 1
    assert data ["status"] == "PENDING"


def test_duplicate_loan_returns_409(client):
    client = client.post("api/loans",json= payload())
    response = client.post("api/loans",json= payload())

    assert response.status_code == 409
    assert "exists" in response.json()["detail"].lower()



