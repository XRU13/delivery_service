import pytest
from app.adapters.database.repositories import ParcelRepo


@pytest.mark.asyncio
async def test_get_by_id_and_session(mock_session_execute, parcel_instance):
    fake_session, set_result = mock_session_execute
    set_result('first', parcel_instance)
    repo = ParcelRepo(fake_session)

    result = await repo.get_by_id_and_session(1, 'abc')
    assert result == parcel_instance


@pytest.mark.asyncio
async def test_get_by_name_and_session(mock_session_execute, parcel_instance):
    fake_session, set_result = mock_session_execute
    set_result('first', parcel_instance)
    repo = ParcelRepo(fake_session)

    result = await repo.get_by_name_and_session('Box', 'abc')
    assert result == parcel_instance


@pytest.mark.asyncio
async def test_get_all_types(mock_session_execute, parcel_type_instance):
    fake_session, set_result = mock_session_execute
    set_result('all', [parcel_type_instance])
    repo = ParcelRepo(fake_session)

    result = await repo.get_all_types()
    assert result == [parcel_type_instance]


@pytest.mark.asyncio
async def test_list_by_filters(mock_session_execute, parcel_instance):
    fake_session, set_result = mock_session_execute
    set_result('all', [parcel_instance])
    repo = ParcelRepo(fake_session)

    result = await repo.list_by_filters('abc', None, None, 10, 0)
    assert result == [parcel_instance]


@pytest.mark.asyncio
async def test_create_parcel(mock_repo_with_create_parcel, parcel_instance):
    result = await mock_repo_with_create_parcel.create_parcel(parcel_instance)

    assert result == 1


@pytest.mark.asyncio
async def test_get_unpriced_parcels(mock_session_execute, parcel_instance):
    fake_session, set_result = mock_session_execute
    set_result('all', [parcel_instance])

    repo = ParcelRepo(fake_session)
    result = await repo.get_unpriced_parcels()

    assert result == [parcel_instance]
