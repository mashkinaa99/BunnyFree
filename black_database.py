import sqlite3


class BlackDataBase:

    def __init__(self, file: str, name_table: str):
        self.file = file
        self.name_table = name_table
        self.conn = sqlite3.connect(self.file)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def create_table(self, rows: str):
        self.cursor.execute(
            f"""CREATE TABLE '{self.name_table}' ({rows});""")

    def recording(self, name: str, test: str):
        self.cursor.execute(f"""SELECT name, test FROM '{self.name_table}' WHERE name = '{name}';""")
        exist = self.cursor.fetchone()

        if exist is not None:
            if test not in exist:
                self.update_test(name, test)
            else:
                return 'Such data already exists'
        else:
            self.cursor.execute(
                f"""INSERT INTO '{self.name_table}' (name, test) VALUES ('{name}', '{test}');""")
            self.conn.commit()

    def delete_company(self, id: int):
        sql = f"""delete from '{self.name_table}' where id={id};"""
        self.cursor.execute(sql)
        self.conn.commit()

    def select_all_data(self):
        sql = f"""SELECT * FROM '{self.name_table}';"""
        recs = self.cursor.execute(sql)
        return recs.fetchall()

    def select_order_data(self):
        sql = f"""SELECT * FROM '{self.name_table}' ORDER BY name ASC, test;"""
        recs = self.cursor.execute(sql)
        return recs.fetchall()

    def update_id(self):
        sql = f"""SELECT id FROM '{self.name_table}' ORDER BY name ASC, test;"""
        recs = self.cursor.execute(sql).fetchall()
        for i in range(1, len(recs)):
            sql_u = f"""UPDATE '{self.name_table}' SET id={i} WHERE id={recs[i - 1][0]}"""
            self.cursor.execute(sql_u)
        self.conn.commit()

    def update_test(self, name: str, test: str):
        sql = f"""SELECT test FROM '{self.name_table}' ORDER BY name ASC, test;"""
        recs = self.cursor.execute(sql).fetchall()
        for company in recs:
            sql_u = f"""UPDATE '{self.name_table}' SET test='{test}' WHERE name='{name}'"""
            self.cursor.execute(sql_u)
        self.conn.commit()

    def search_by_test(self, test: str):
        sql = f"""SELECT * FROM '{self.name_table}' WHERE test='{test}';"""
        recs = self.cursor.execute(sql).fetchall()
        return recs

    def search_by_name(self, name: str):
        sql = f"""SELECT name, test FROM '{self.name_table}' WHERE name LIKE '%{name}%';"""
        recs = self.cursor.execute(sql).fetchall()
        if len(recs) < 1:
            sql = f"""SELECT name, test FROM '{self.name_table}' WHERE name LIKE '%{name.title()}%';"""
            recs = self.cursor.execute(sql).fetchall()
        return recs
