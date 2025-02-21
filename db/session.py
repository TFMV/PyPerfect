import ibis
from pathlib import Path

class DatabaseSession:
    """Manages the DuckDB connection using Ibis."""
    
    _instance = None
    DB_PATH = Path("data/pyperfect.duckdb")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = ibis.duckdb.connect(str(cls.DB_PATH))
        return cls._instance

    def get_connection(self):
        """Returns the active Ibis connection."""
        return self.conn

# Singleton instance
db_session = DatabaseSession()
