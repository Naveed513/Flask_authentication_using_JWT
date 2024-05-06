import pyodbc
# import uuid


class UserDatabase:
    def __init__(self):
        self.cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=Naveed\SQLEXPRESS;DATABASE=caffe;')
        self.cursor = self.cnxn.cursor()

    def get_user(self, user_id):
        query = "SELECT * FROM users WHERE id=?;"
        self.cursor.execute(query, (user_id))
        result = self.cursor.fetchone()
        user_dict = {}
        if not result is None:
            user_dict['id'], user_dict['username'], user_dict['password'] = result
        return user_dict

    def add_user(self, username, password):
        query = "INSERT INTO users(username, password) VALUES(?, ?);"
        # user_id = uuid.uuid4().hex
        try:
            self.cursor.execute(query, (username, password))
            self.cnxn.commit()
            return self.cursor.rowcount
        except pyodbc.IntegrityError:
            return False

        # return self.cursor.rowcount
        # return 'Record inserted successfully.'

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE id=?"
        self.cursor.execute(query, (user_id))
        self.cnxn.commit()
        return self.cursor.rowcount

    def verify_user(self, username, password):
        query = "SELECT id FROM users WHERE username=? AND password=?;"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]


# db = UserDatabase()
# db.delete_user(user_id=1)
