def test_endpoint_index(client):
    """
    test if all json endpoints are listed
    :param client:
    :return:
    """
    # get response
    response = client.get("/api/v1/endpoints/")
    assert response.status_code == 200
    assert response.is_json
    # test if list includes all endpoints
    assert b"demo" in response.data
