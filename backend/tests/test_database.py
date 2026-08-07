"""Database lifecycle and unit-of-work tests without a database server."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from app.database import session as session_module
from app.database.unit_of_work import SQLAlchemyUnitOfWork


@pytest.mark.anyio
async def test_close_db_disposes_and_resets_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine = MagicMock()
    engine.dispose = AsyncMock()
    monkeypatch.setattr(session_module, "_engine", engine)
    monkeypatch.setattr(session_module, "_AsyncSessionLocal", MagicMock())
    await session_module.close_db()
    engine.dispose.assert_awaited_once()
    assert session_module._engine is None
    assert session_module._AsyncSessionLocal is None


@pytest.mark.anyio
async def test_check_db_is_false_when_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(session_module, "_AsyncSessionLocal", None)
    assert await session_module.check_db() is False


@pytest.mark.anyio
async def test_unit_of_work_commits_and_closes() -> None:
    db_session = MagicMock()
    db_session.commit = AsyncMock()
    db_session.rollback = AsyncMock()
    db_session.close = AsyncMock()
    unit = SQLAlchemyUnitOfWork(MagicMock(return_value=db_session))
    async with unit:
        await unit.commit()
    db_session.commit.assert_awaited_once()
    db_session.close.assert_awaited_once()


@pytest.mark.anyio
async def test_unit_of_work_rolls_back_exception() -> None:
    db_session = MagicMock()
    db_session.rollback = AsyncMock()
    db_session.close = AsyncMock()
    unit = SQLAlchemyUnitOfWork(MagicMock(return_value=db_session))
    await unit.__aenter__()
    await unit.__aexit__(RuntimeError, RuntimeError("failed"), None)
    db_session.rollback.assert_awaited_once()
