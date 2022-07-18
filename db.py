import sqlite3

class Database:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()    
    def add_users_table(self):
        with self.connection:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS "users" (
                "id"	INTEGER,
                "user_id"	INTEGER NOT NULL,
                "user_money"	INTEGER NOT NULL DEFAULT '0',
                PRIMARY KEY("id" AUTOINCREMENT));''')

    def add_bill_table(self):
        with self.connection:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS "bill" (
                "id"	INTEGER,
                "user_id"	INTEGER NOT NULL,
                "user_bill_id"	INTEGER NOT NULL,
                "bill_money"	INTEGER NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT));''')

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))
    def add_user(self, user_id):
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id) VALUES(?)", (user_id,))
    def add_user_money(self, user_money, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users SET user_money = ? WHERE user_id = ?", (user_money, user_id,))
    def user_money(self, user_id):
        with self.connection:
            return(self.cursor.execute("SELECT user_money FROM users WHERE user_id = ?", (user_id,)).fetchone()[0])
    
    def add_user_bill_id(self, user_id, user_bill_id, bill_money):
        with self.connection:
            self.cursor.execute("INSERT INTO bill (user_id, user_bill_id, bill_money) VALUES(?,?,?)", (user_id, user_bill_id, bill_money))
    def user_bill_id_exists(self, user_bill_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM bill WHERE user_bill_id = ?", (user_bill_id,)).fetchall()
            return bool(len(result))
    def bill_money(self, user_bill_id):
        with self.connection:
            return(self.cursor.execute("SELECT bill_money FROM bill WHERE user_bill_id = ?", (user_bill_id,)).fetchone()[0])
    def dell_user_bill_id(self, user_bill_id):
        with self.connection:
            return(self.cursor.execute("DELETE FROM bill WHERE user_bill_id = ?", (user_bill_id,)))