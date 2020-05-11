import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    # making sure that only price should be updated if item already exists
    parser.add_argument('price',
      type = float,
      required = True,
      help = "The field 'price' is empty or not given float value."
    )

    @jwt_required()
    def get(self, name):
        try:
            # we can also write self.find_by_name(name), it is allowed in @classmethod
            item = Item.find_by_name(name)
            if item:
                return item
            return {'message': '{} does not exists.'.format(name.title())}, 404
        except:
            return {'message': 'An error occured while searching.'}, 500

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        if Item.find_by_name(name):
            return {'message': '{} already exists. Try another.'.format(name.title())}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            Item.insert(item)
        except:
            return {'message': 'An error occured while inserting.'}, 500

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': '{} successfully deleted.'.format(name.title())}

    def put(self, name):
        # this line of code will only let price to be passed in data
        data = Item.parser.parse_args()

        item = Item.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {'message': 'An error occured while inserting.'}, 500
        else:
            try:
                Item.update(updated_item)
            except:
                return {'message': 'An error occured while updating.'}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            item = {'name': row[0], 'price': row[1]}
            items.append(item)

        connection.close()

        return {'items': items}
