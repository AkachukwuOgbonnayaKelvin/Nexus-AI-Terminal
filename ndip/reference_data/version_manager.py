class VersionManager:
    def increment(self, current_version: int) -> int:
        return current_version + 1 if current_version else 1
