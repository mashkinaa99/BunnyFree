import sqlite3


class BlackDataBase:

    def __init__(self, file: str, name_table: str):
        self.file = file
        self.name_table = name_table
        self.conn = sqlite3.connect(self.file)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def create_table(self, rows: str):  # Creates a new table
        sql = """CREATE TABLE '{}' ({});""".format(self.name_table, rows)
        self.cursor.execute(sql)

    def recording(self, name: str, test: str):  # Adds a company to the database
        sql = """SELECT name, test FROM {} WHERE name = '{}';""".format(self.name_table, name)
        self.cursor.execute(sql)
        exist = self.cursor.fetchone()

        if exist is not None:
            if test not in exist:
                self.update_test(name, test)
            else:
                return 'Such data already exists'
        else:
            sql = """INSERT INTO {} (name, test) VALUES ('{}', '{}');""".format(self.name_table, name, test)
            self.cursor.execute(sql)
            self.conn.commit()

    def delete_company(self, id: int):  # Removes a company from the database
        sql = """DELETE FROM {} WHERE id={};""".format(self.name_table, id)
        self.cursor.execute(sql)
        self.conn.commit()

    def select_all_data(self):  # Shows all records in the database
        sql = """SELECT * FROM {};""".format(self.name_table)
        recs = self.cursor.execute(sql)
        return recs.fetchall()

    def select_order_data(self):  # Shows all records in the database (sorted by name and test)
        sql = """SELECT * FROM {} ORDER BY name ASC, test;""".format(self.name_table)
        recs = self.cursor.execute(sql)
        return recs.fetchall()

    def update_id(self):  # Change id for all elements (starting with 1 and ending with the number of records)
        sql = """SELECT id FROM {} ORDER BY name ASC, test;""".format(self.name_table)
        recs = self.cursor.execute(sql).fetchall()
        for i in range(1, len(recs)):
            sql_u = """UPDATE {} SET id={} WHERE id={}""".format(self.name_table, i, recs[i - 1][0])
            self.cursor.execute(sql_u)
        self.conn.commit()

    def search_id(self, name):  # Search for company id by name
        sql = """SELECT id, name, test FROM {} WHERE name='{}'""".format(self.name_table, name)
        recs = self.cursor.execute(sql).fetchall()
        return recs

    def update_test(self, name: str, test: str):  # Updates the company test
        sql = """SELECT test FROM {} ORDER BY name ASC, test;""".format(self.name_table)
        recs = self.cursor.execute(sql).fetchall()
        for company in recs:
            sql = """UPDATE {} SET test='{}' WHERE name='{}'""".format(self.name_table, test, name)
            self.cursor.execute(sql)
        self.conn.commit()

    def search_by_test(self, test: str):  # Shows companies with the same test
        sql = """SELECT * FROM {} WHERE test='{}';""".format(self.name_table, test)
        recs = self.cursor.execute(sql).fetchall()
        return recs

    def search_by_name(self, name: str):  # Shows the companies the name belongs to
        sql = """SELECT name, test FROM {} WHERE name LIKE '%{}%';""".format(self.name_table, name)
        recs = self.cursor.execute(sql).fetchall()
        if len(recs) < 1:
            sql = """SELECT name, test FROM {} WHERE name LIKE '%{}%';""".format(self.name_table, name.title())
            recs = self.cursor.execute(sql).fetchall()
        return recs


if __name__ == '__main__':
    b = BlackDataBase('black_database.db', 'blacktable')
    print(b.search_by_name('Loreal'))
