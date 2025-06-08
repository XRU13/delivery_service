import pytest
from httpx import AsyncClient
from fastapi import status



@pytest.mark.asyncio
async def test_create_parcel_success(test_client):
    response = await test_client.post(
        '/parcels/',
        json={
            'name': 'Box',
            'weight': 1.2,
            'type_id': 1,
            'content_value_usd': 50.0
        }
    )
    assert response.status_code == 201
    assert 'parcel_id' in response.json()


@pytest.mark.asyncio
async def test_get_parcels_list(test_client: AsyncClient):
    response = await test_client.get('/parcels/')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_parcel_by_id(test_client: AsyncClient):
    post_response = await test_client.post(
        '/parcels/',
        json={
            'name': 'Box',
            'weight': 2.5,
            'type_id': 1,
            'content_value_usd': 100.0,
        }
    )
    parcel_id = post_response.json()['parcel_id']

    response = await test_client.get(f'/parcels/{parcel_id}')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['parcel_id'] == parcel_id
    assert data['name'] == 'Box'
