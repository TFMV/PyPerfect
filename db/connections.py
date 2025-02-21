# db/connection.py
import ibis
from core.config import settings

class Database:
    def __init__(self):
        self.connection = ibis.duckdb.connect(settings.DATABASE_URL)

    def get_connection(self):
        return self.connection

db = Database()
