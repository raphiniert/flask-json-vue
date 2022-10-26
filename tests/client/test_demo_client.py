def test_demo_client_index(client):
    """
    test demo client index
    :param client:
    :return:
    """
    # get response
    response = client.get("/")
    # assert status code
    assert response.status_code == 200
