import pyodbc
import uuid


class ItemDatabase:
    def __init__(self):
        self.cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=Naveed\SQLEXPRESS;DATABASE=caffe;')
        self.cursor = self.cnxn.cursor()

    def _get_items(self, item_list):
        items_list_dict = []
        for item in item_list:
            item_d = {}
            item_d['id'], item_d['name'], item_d['price'] = item
            items_list_dict.append(item_d)
        return items_list_dict

    def get_items(self):
        result = []
        query = "SELECT * FROM items;"
        self.cursor.execute(query)
        result = self._get_items(self.cursor.fetchall())
        return result

    def get_item(self, item_id):
        query = f"SELECT * FROM items WHERE id='{item_id}';"
        self.cursor.execute(query)
        result = self._get_items(self.cursor.fetchall())
        return result

    def add_item(self, body):
        query = "INSERT INTO items VALUES(?, ?, ?);"
        item_id = uuid.uuid4().hex
        self.cursor.execute(query, (item_id, body['name'], body['price']))
        self.cnxn.commit()
        # return self.cursor.rowcount
        # return 'Record inserted successfully.'

    def update_item(self, item_id, body):
        query = "UPDATE items SET name=?, price=? Where id=?;"
        self.cursor.execute(query,(body['name'], body['price'], item_id))
        self.cnxn.commit()
        return self.cursor.rowcount

    def delete_item(self, item_id):
        query = "DELETE FROM items WHERE id=?"
        self.cursor.execute(query, (item_id))
        self.cnxn.commit()
        return self.cursor.rowcount

# db = ItemDatabase()
# db.put_item(item_id='56a412b694c24760864c25971b6e5f6c', body={'name':'Cashew', 'price':339})
