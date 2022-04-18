def test_demo_client_index(client):
    """
    test demo client index
    :param client:
    :return:
    """
    # get response
    response = client.get("/demo/")
    # assert status code
    assert response.status_code == 200
    # assert content
    assert b"<h1>This is the demo index page.</h1>" in response.data
