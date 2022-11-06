import pytest


URL_PREFIX = "/api/v1/address"


@pytest.mark.parametrize(
    ("endpoint",),
    (("detail",), ("create",), ("update",), ("delete",), ("array",)),
)
def test_address_scheme(client, endpoint):
    """
    test if all json scheme endpoints are defined and a json response is returned
    :param client:
    :param endpoint:
    :return:
    """
    response = client.get(f"{URL_PREFIX}/schema/{endpoint}.schema.json")
    assert response.status_code == 200
    assert response.is_json


def test_address_api_add(client):
    """
    TODO:
    :param client:
    """
    response = client.post(f"{URL_PREFIX}/add", json={"street": "Street Name"})

    assert response.status_code == 201
    assert response.is_json
    assert b"Created new address with id: 3" in response.data


def test_address_api_get(client):
    """
    TODO:
    :param client:
    """
    response = client.get(f"{URL_PREFIX}/get/1")
    assert response.status_code == 200
    assert response.is_json
    assert b'"id": 1' in response.data


def test_address_update(client):
    """
    TODO:
    :param client:
    """
    response = client.patch(
        f"{URL_PREFIX}/update",
        json={"id": 1, "street": "Fake Street Name"},
    )
    assert response.status_code == 200
    assert response.is_json
    assert b"Updated address with id: 1" in response.data


def test_address_delete(client):
    """
    TODO:
    :param client:
    """
    response = client.delete(
        f"{URL_PREFIX}/delete",
        json={"id": 1},
    )
    assert response.status_code == 200
    assert response.is_json
    assert b"Deleted address with id: 1" in response.data


def test_address_api_list(client):
    """
    test address api list
    :param client:
    :return:
    """
    # get response
    response = client.get("/api/v1/address/list")
    # assert status code
    assert response.status_code == 200
    # asser response is json
    assert response.is_json
    # assert content is not an empty list
    assert response.json != []
