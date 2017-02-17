import sqlite3


class DBhelper:
    def __init__(self, dbname= "todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, item_text, owner):
        stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text, owner):
        stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, owner):
        stmt = "SELECT description FROM items WHERE owner = (?)"
        args = (owner,)
        return [x[0] for x in self.conn.execute(stmt, args)]

    def delete_all(self, owner):
        stmt = "DELETE FROM items WHERE owner = (?)"
        args = (owner, )
        self.conn.execute(stmt, args)
        self.conn.commit()