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
    assert b'<list-component obj-type="demo"></list-component>' in response.data
