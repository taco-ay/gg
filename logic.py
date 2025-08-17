# logic.py
import sqlite3
from config import DATABASE


class DB_Manager:
    def __init__(self, database=DATABASE):
        self.database = database

    def __execute(self, sql, params=()):
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()
        cur.execute(sql, params)
        data = cur.fetchall()
        conn.close()
        return data

    def get_books(self, limit=5):
        sql = "SELECT ISBN, `Book-Title`, `Book-Author` FROM books LIMIT ?"
        return self.__execute(sql, (limit,))

    def get_users(self, limit=5):
        sql = "SELECT `User-ID`, Location, Age FROM users LIMIT ?"
        return self.__execute(sql, (limit,))

    def get_ratings(self, limit=5):
        sql = "SELECT `User-ID`, ISBN, `Book-Rating` FROM ratings LIMIT ?"
        return self.__execute(sql, (limit,))

    def run_sql(self, query):
        """Serbest SQL sorgusu çalıştırmak için"""
        return self.__execute(query)
