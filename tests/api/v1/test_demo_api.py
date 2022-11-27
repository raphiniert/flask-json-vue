import pytest


URL_PREFIX = "/api/v1/demo"


@pytest.mark.parametrize(
    ("endpoint",),
    (("detail",), ("create",), ("update",), ("delete",), ("array",)),
)
def test_demo_scheme(client, endpoint):
    """
    test if all json scheme endpoints are defined and a json response is returned
    :param client:
    :param endpoint:
    :return:
    """
    response = client.get(f"{URL_PREFIX}/schema/{endpoint}.schema.json")
    assert response.status_code == 200
    assert response.is_json


def test_demo_api_add(client):
    """
    TODO:
    :param client:
    """
    response = client.post(
        f"{URL_PREFIX}/add",
        json={
            "address_id": None,
            "name": "Test Name",
            "entry_date": "2022-01-01T00:00:00+01:00",
            "decimal_value": 1.0,
        },
    )

    assert response.status_code == 201
    assert response.is_json
    assert b"Created new demo with id: 4" in response.data


def test_demo_api_get(client):
    """
    TODO:
    :param client:
    """
    response = client.get(f"{URL_PREFIX}/get/1")
    assert response.status_code == 200
    assert response.is_json
    assert b'"id": 1' in response.data


def test_demo_update(client):
    """
    TODO:
    :param client:
    """
    response = client.patch(
        f"{URL_PREFIX}/update",
        json={
            "id": 1,
            "address_id": None,
            "name": "Demo",
            "entry_date": "2022-01-01T00:00:01+01:00",
            "decimal_value": 100.0,
        },
    )
    assert response.status_code == 200
    assert response.is_json
    assert b"Updated demo with id: 1" in response.data


def test_demo_delete(client):
    """
    TODO:
    :param client:
    """
    response = client.delete(
        f"{URL_PREFIX}/delete",
        json={
            "id": 1,
        },
    )
    assert response.status_code == 200
    assert response.is_json
    assert b"Deleted demo with id: 1" in response.data


def test_demo_api_list(client):
    """
    test demo api list
    :param client:
    :return:
    """
    # get response
    response = client.get("/api/v1/demo/list")
    # assert status code
    assert response.status_code == 200
    # asser response is json
    assert response.is_json
    # assert content is not an empty list
    assert response.json != []
