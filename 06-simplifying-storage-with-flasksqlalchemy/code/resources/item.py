import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

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
            item = ItemModel.find_by_name(name)
            if item:
                return item.json()
            return {'message': '{} does not exists.'.format(name.title())}, 404
        except:
            return {'message': 'An error occured while searching.'}, 500

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': '{} already exists. Try another.'.format(name.title())}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {'message': 'An error occured while inserting.'}, 500

        return item.json(), 201

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

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {'message': 'An error occured while inserting.'}, 500
        else:
            try:
                updated_item.update()
            except:
                return {'message': 'An error occured while updating.'}, 500
        return updated_item.json()


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
