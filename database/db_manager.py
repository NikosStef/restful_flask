import sqlite3
import sys
from sqlite3 import Error

DB = 'database/database.db'

class DbManager():

    def __init__(self):
        self.conn = sqlite3.connect(DB, check_same_thread=False)

    def get_all(self):
        self.conn.cursor().execute('''SELECT * FROM notes;''')
        return self.conn.cursor().fetchall()

    def add_note(self, note):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO notes VALUES (?, ?, ?);''', (note.context, note.archived, note.ownerEmail))
        self.conn.commit()
        return cursor.execute('''SELECT max(ROWID) FROM notes;''').fetchone()

    def get_note(self, id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT ROWID, * FROM notes WHERE ROWID = ?;''', (id,))
        return cursor.fetchone()

    def delete_note(self, id):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM notes WHERE ROWID = ?;''', (id,))
        self.conn.commit()

    def fetch_notes(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM notes''')
        return cursor.fetchall()

    def archive_note(self, id):
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE notes SET archived = 1 WHERE ROWID = ?;''', (id,))
        self.conn.commit()

    def unarchive_note(self, id):
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE notes SET archived = 0 WHERE ROWID = ?;''', (id,))
        self.conn.commit()

    def update_note_context(self, note):
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE notes SET context = ? WHERE ROWID = ?;''', (note.context, note.id))

    def get_user(self, email):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT ROWID, * FROM users WHERE email = ?;''', (email,))
        return cursor.fetchone()

    def get_user_by_id(self, id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT ROWID, * FROM users WHERE ROWID = ?;''', (id,))
        return cursor.fetchone()

    def add_user(self, user):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO users VALUES (NULL, ?, ?, ?);''', (user.username, user.password, user.email))
        except sqlite3.IntegrityError:
            return None
        finally:
            self.conn.commit()
            return cursor.execute('''SELECT max(ROWID) FROM users;''').fetchone()

    def execute(self, command):
        cursor = self.conn.cursor()
        cursor.execute(command)

    def execute_with_commit(self, command):
        cursor = self.conn.cursor()
        cursor.execute(command)
        self.self.conn.commit()

    def close(self):
        self.conn.close()
