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
