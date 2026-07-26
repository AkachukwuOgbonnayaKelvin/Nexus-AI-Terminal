"""Metadata Warehouse – writes to registries with dynamic INSERT."""

import json
import uuid
from datetime import datetime
from typing import Any

from ndip.utils.db_connector import execute, fetch, fetchrow


class MetadataWarehouse:
    """Enterprise Metadata Warehouse with versioning and registry separation."""

    def __init__(self):
        self.schema = "metadata"
        self.allowed_fields = [
            "symbol",
            "display_symbol",
            "short_name",
            "long_name",
            "description",
            "isin",
            "cusip",
            "sedol",
            "ric",
            "bloomberg_ticker",
            "figi",
            "asset_class",
            "sub_asset_class",
            "instrument_type",
            "sector",
            "industry",
            "sub_industry",
            "theme",
            "strategy_group",
            "market_category",
            "exchange_code",
            "base_currency",
            "quote_currency",
            "settlement_currency",
            "profit_currency",
            "margin_currency",
            "tick_size",
            "tick_value",
            "point_size",
            "digits",
            "lot_size",
            "min_volume",
            "max_volume",
            "volume_step",
            "contract_size",
            "market_open",
            "market_close",
            "trading_days",
            "holiday_calendar",
            "session_type",
            "timezone",
            "dst_rules",
            "expiration",
            "first_notice",
            "settlement_date",
            "underlying",
            "multiplier",
            "option_type",
            "strike",
            "price_precision",
            "price_format",
            "tick_format",
            "pip_size",
            "fraction_display",
            "margin_requirement",
            "leverage_group",
            "swap_long",
            "swap_short",
            "swap_mode",
            "commission_group",
            "avg_daily_volume",
            "avg_spread",
            "liquidity_score",
            "volatility_score",
            "market_cap",
            "outstanding_shares",
            "float_shares",
            "company_id",
            "quality_score",
            "verified",
            "provider",
            "provider_rank",
            "checksum",
            "country_code",
            "sector_id",
            "industry_id",
            "asset_type_id",
        ]

    def _get_insertable_fields(self, record: dict[str, Any]) -> dict[str, Any]:
        return {
            k: v
            for k, v in record.items()
            if k in self.allowed_fields and v is not None
        }

    async def store_asset(self, record: dict[str, Any], source: str) -> dict[str, Any]:
        symbol = record.get("symbol")
        if not symbol:
            return {"error": "Missing symbol"}

        existing = await fetchrow(
            f"SELECT asset_id, version FROM {self.schema}.asset_registry WHERE symbol = $1",
            symbol,
        )

        fields = self._get_insertable_fields(record)
        if "provider" not in fields:
            fields["provider"] = source
        if "provider_rank" not in fields:
            fields["provider_rank"] = 1

        if existing:
            asset_id = existing["asset_id"]
            current_version = existing["version"]
            new_version = int(current_version) + 1
            # Build UPDATE dynamically
            set_clauses = []
            params = []
            idx = 1
            for field, value in fields.items():
                if field in ["asset_id", "symbol", "last_updated", "version"]:
                    continue
                set_clauses.append(f"{field} = ${idx}")
                params.append(value)
                idx += 1
            set_clauses.append(f"version = ${idx}")
            params.append(new_version)
            idx += 1
            set_clauses.append("last_updated = NOW()")
            params.append(asset_id)
            query = f"""
                UPDATE {self.schema}.asset_registry
                SET {", ".join(set_clauses)}
                WHERE asset_id = ${idx}
                RETURNING asset_id
            """
            await execute(query, *params)
            await self._record_version(asset_id, new_version, record)
            return {
                "stored": True,
                "asset_id": asset_id,
                "version": new_version,
                "action": "updated",
            }
        else:
            asset_id = uuid.uuid4()
            fields["asset_id"] = asset_id
            # Build INSERT
            columns = []
            placeholders = []
            params = []
            idx = 1
            for field, value in fields.items():
                if field == "version":
                    continue
                columns.append(field)
                placeholders.append(f"${idx}")
                params.append(value)
                idx += 1
            columns.append("version")
            placeholders.append(f"${idx}")
            params.append(1)
            idx += 1
            columns_str = ", ".join(columns)
            placeholders_str = ", ".join(placeholders)
            query = f"""
                INSERT INTO {self.schema}.asset_registry ({columns_str})
                VALUES ({placeholders_str})
                RETURNING asset_id
            """
            await execute(query, *params)
            await self._record_version(asset_id, 1, record)
            return {
                "stored": True,
                "asset_id": asset_id,
                "version": 1,
                "action": "inserted",
            }

    async def _record_version(
        self, asset_id: str, version: int, record: dict[str, Any]
    ):
        """Log version history with proper JSON serialization."""
        # Convert UUIDs and other non-serializable types to strings
        serializable = {}
        for k, v in record.items():
            if isinstance(v, uuid.UUID):
                serializable[k] = str(v)
            elif isinstance(v, datetime) or hasattr(v, "isoformat"):
                serializable[k] = v.isoformat()
            else:
                serializable[k] = v
        query = f"""
            INSERT INTO {self.schema}.version_history (asset_id, version, changed_fields, changed_by)
            VALUES ($1, $2, $3, $4)
        """
        await execute(
            query,
            asset_id,
            version,
            json.dumps(serializable, default=str),
            "metadata_engine",
        )

    async def get_asset(self, symbol: str) -> dict[str, Any] | None:
        row = await fetchrow(
            f"SELECT * FROM {self.schema}.asset_registry WHERE symbol = $1", symbol
        )
        return dict(row) if row else None

    async def get_asset_by_uuid(self, asset_id: str) -> dict[str, Any] | None:
        row = await fetchrow(
            f"SELECT * FROM {self.schema}.asset_registry WHERE asset_id = $1", asset_id
        )
        return dict(row) if row else None

    async def search_assets(
        self, query: str, asset_class: str = None, limit: int = 20
    ) -> list[dict[str, Any]]:
        sql = f"SELECT * FROM {self.schema}.asset_registry WHERE symbol ILIKE $1 OR long_name ILIKE $1"
        params = [f"%{query}%"]
        if asset_class:
            sql += " AND asset_class = $2"
            params.append(asset_class)
        sql += f" LIMIT {limit}"
        rows = await fetch(sql, *params)
        return [dict(row) for row in rows]

    async def get_stats(self) -> dict[str, Any]:
        count = await fetchrow(f"SELECT COUNT(*) FROM {self.schema}.asset_registry")
        return {"total_assets": count[0] if count else 0}
