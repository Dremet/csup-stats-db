import psycopg2
from decouple import config


class Cursor:
    def __init__(self) -> None:
        self.host, self.dbname, self.user, self.password = config("PGHOST"),config("PGDBNAME"),config("PGUSER"),config("PGPASSWORD")
    
    def __enter__(self):
        self.conn = psycopg2.connect(f"host={self.host} dbname={self.dbname} user={self.user} password={self.password}")
        self.conn.set_session(autocommit=True)

        self.cur = self.conn.cursor()

        return self.cur
    
    def __exit__(self, type, value, traceback):
        self.conn.close()

