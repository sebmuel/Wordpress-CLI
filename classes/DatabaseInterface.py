from .Config import WpConfig
import mysql.connector


class DatabaseInterface:

    def __init__(self) -> None:
        self.config = WpConfig()
        self.db_host = self.config.cnf.get("db_host")
        self.db_user = self.config.cnf.get("db_user")
        self.db_pw = self.config.cnf.get("db_pw")
        self.db = self.config.cnf.get("db")

    def load_from_db(self, sql: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        return result

    def save_to_db(self, sql: str, values: tuple, multi=False):
        if not values:
            return None
        conn = self.get_connection()
        cursor = conn.cursor()
        if not multi:
            cursor.execute(sql, values)
        else:
            values = [x for x in values]
            cursor.executemany(sql, values)
        conn.commit()
        conn.close()

    def get_connection(self):
        return mysql.connector.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_pw,
            database=self.db,
            charset="utf8"
        )
    """concrete load implementation"""    
    def load(self):
        pass
    
    """concrete create implementation"""    
    def create(self):
        pass
