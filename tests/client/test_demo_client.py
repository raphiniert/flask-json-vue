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


def test_demo_client_create(client):
    """
    test demo client index
    :param client:
    :return:
    """
    # get response
    response = client.get("/demo/add")
    # assert status code
    assert response.status_code == 200
    # assert content
    assert b'<detail-component obj-type="demo"></detail-component>' in response.data


def test_demo_client_update(client):
    """
    test demo client index
    :param client:
    :return:
    """
    # get response
    response = client.get(f"/demo/update/{1}")
    # assert status code
    assert response.status_code == 200
    # assert content
    assert (
        b'<detail-component obj-type="demo" :obj-id="1"></detail-component>'
        in response.data
    )
