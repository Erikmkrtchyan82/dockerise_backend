import logging
import psycopg2


class Postgres:
    def __init__(self, **params):
        logging.info("Connecting to the PostgreSQL database...")
        self.conn = psycopg2.connect(**params)
        self.cur = self.conn.cursor()
        self.conn.commit()

    def __del__(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            logging.info("Database connection closed.")


    def cleanup(self):
        self.cur.execute("DROP SCHEMA public CASCADE;")
        self.cur.execute("CREATE SCHEMA public;")
        self.conn.commit()


    def create_tables(self):
        tables = [
                    """
                    CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY generated always as identity,
                        name TEXT NOT NULL,
                        surename TEXT NOT NULL,
                        age INTEGER NOT NULL
                    );
                    """
                ]
        for table in tables:
            self.cur.execute(table)
        self.conn.commit()

    def select(self, table_name: str, key: str = "*", data: dict = None, additinal_query = "") -> list:
        query = [
            f"SELECT {key} FROM {table_name}",
            f"WHERE ({','.join(data.keys())}) = ({','.join(data.values())})" if data else "",
            additinal_query,
            ";"
        ]
        self.cur.execute(" ".join(query))
        return self.cur.fetchall()
        

    def insert(self, table_name: str, data: dict, additinal_query = "") -> str:
        query = [
            f"INSERT INTO {table_name}({', '.join(data.keys())})",
            "VALUES ({})".format(', '.join((f"'{val}'" if isinstance(val, str) else str(val) for val in data.values()))),
            additinal_query,
            ";"
        ]

        self.cur.execute(" ".join(query))
        info = self.cur.fetchone()
        self.conn.commit()
        
        return info

    def delete(self, table_name: str, data: dict) -> None:
        query = [
            f"DELETE FROM {table_name}",
            "WHERE ({column_names}) = ({values})".format(
                column_names = ", ".join(data.keys()),
                values = ", ".join((f"'{val}'" if isinstance(val, str) else str(val) for val in data.values()))),
            ";"
        ]

        self.cur.execute(" ".join(query))
        self.conn.commit()
