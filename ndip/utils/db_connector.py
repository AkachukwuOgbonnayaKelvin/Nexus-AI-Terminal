"""Database connection pool for NDIP warehouses."""

from typing import List, Optional

import asyncpg
from asyncpg import Pool, Record

from foundation.config import config

_pool: Optional[Pool] = None


async def get_pool() -> Pool:
    """Get or create a connection pool."""
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            config.DATABASE_URL, min_size=5, max_size=20, command_timeout=30
        )
    return _pool


async def close_pool() -> None:
    """Close the connection pool."""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


async def execute(query: str, *args) -> str:
    """Execute a query and return status."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.execute(query, *args)


async def fetch(query: str, *args) -> List[Record]:
    """Fetch multiple rows."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetch(query, *args)


async def fetchrow(query: str, *args) -> Optional[Record]:
    """Fetch a single row."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, *args)
