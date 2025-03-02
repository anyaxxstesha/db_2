from unittest.mock import AsyncMock, Mock

import pytest


@pytest.fixture
def db_session():
    session = AsyncMock()
    session.scalars.return_value = Mock()
    return session
