import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from app.adapters.database.repositories import ParcelRepo
from app.applications.dataclasses.parcel_dataclasses import Parcel, ParcelType


@pytest.fixture
def mock_session_execute():
    session = AsyncMock()

    def _set_execute_result(method: str, return_value):
        scalars_mock = MagicMock()
        getattr(scalars_mock, method).return_value = return_value

        result_mock = MagicMock()
        result_mock.scalars.return_value = scalars_mock
        session.execute.return_value = result_mock

    return session, _set_execute_result


@pytest.fixture
def parcel_instance():
    """Готовый экземпляр Parcel с id."""
    return Parcel(
        id=1,
        session_id='abc',
        name='Box',
        weight=1.0,
        type_id=1,
        content_value_usd=100.0,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def parcel_type_instance():
    return ParcelType(
        id=1,
        name='Одежда'
    )


@pytest.fixture
def mock_repo_with_create_parcel(mock_session_execute):
    fake_session, _ = mock_session_execute

    repo = ParcelRepo(fake_session)

    async def fake_create_parcel(*args, **kwargs):
        return 1

    repo.create_parcel = fake_create_parcel
    return repo