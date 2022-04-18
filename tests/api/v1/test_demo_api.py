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
