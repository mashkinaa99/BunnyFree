import sqlite3


class BlackDataBase:

    def __init__(self, file: str, name_table: str):
        self.file = file
        self.name_table = name_table

    def create_table(self, rows: str):
        file = self.file
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
        cursor.execute(
            f"""CREATE TABLE '{self.name_table}' ({rows})""")

    def recording(self, name: str, test: str):
        file = self.file
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
        cursor.execute(f"""SELECT id FROM '{self.name_table}' WHERE name = '{name}'""")
        exist = cursor.fetchone()

        if exist is not None:
            return 'Such a record already exists'

        cursor.execute(
            f"""INSERT INTO '{self.name_table}' (name, test) values('{name}', '{test}')""")

    def commit(self):
        file = self.file
        conn = sqlite3.connect(file)
        conn.commit()

    def delete_company(self, id: int):
        file = self.file
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
        sql = f"""delete from '{self.name_table}' where id={id};"""
        cursor.execute(sql)

    def select_all_data(self):
        file = self.file
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
        sql = f"""SELECT * FROM '{self.name_table}';"""
        recs = cursor.execute(sql)
        return recs.fetchall()

    def select_order_data(self):
        file = self.file
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
        sql = f"""SELECT * FROM '{self.name_table}' ORDER BY name ASC, test;"""
        recs = cursor.execute(sql)
        return recs.fetchall()

    def update_id(self):
        file = self.file
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
        sql = f"""SELECT id FROM '{self.name_table}' ORDER BY name ASC, test;"""
        recs = cursor.execute(sql).fetchall()
        for i in range(1, len(recs)):
            sql_u = f"""UPDATE '{self.name_table}' SET id={i} WHERE id={recs[i - 1][0]}"""
            cursor.execute(sql_u)

    def update_test(self, name: str, test: str):
        file = self.file
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
        sql = """SELECT test FROM '{self.name_table}' ORDER BY name ASC, test;"""
        recs = cursor.execute(sql).fetchall()
        for company in recs:
            sql_u = f"""UPDATE '{self.name_table}' SET test='{test}' WHERE name='{name}'"""
            cursor.execute(sql_u)

    def search_by_test(self, test: str):
        file = self.file
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
        sql = f"""SELECT * FROM '{self.name_table}' WHERE test='{test}';"""
        recs = cursor.execute(sql).fetchall()
        return recs

    def search_by_name(self, name: str):
        file = self.file
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
        sql = f"""SELECT name, test FROM '{self.name_table}' WHERE name LIKE '%{name}%';"""
        recs = cursor.execute(sql).fetchall()
        if len(recs) < 1:
            sql = f"""SELECT name, test FROM '{self.name_table}' WHERE name LIKE '%{name.title()}%';"""
            recs = cursor.execute(sql).fetchall()
        return recs



