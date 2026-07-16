from ndip.utils.db_connector import execute


class AuditManager:
    async def log(self, action: str, table: str, record_id: str, details: dict):
        query = """
            INSERT INTO metadata.audit_log (action, table_name, record_id, details, changed_at)
            VALUES ($1, $2, $3, $4, NOW())
        """
        await execute(query, action, table, record_id, details)
