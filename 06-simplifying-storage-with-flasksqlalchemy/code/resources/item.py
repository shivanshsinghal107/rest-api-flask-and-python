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
    parser.add_argument('store_id',
      type = int,
      required = True,
      help = "Every item needs 'store_id'."
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
        # we can also write item = ItemModel(name, data['price'], data['store_id'])
        # here price and store_idare key value arguments so pass data as **kwargs
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured while inserting.'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': '{} successfully deleted.'.format(name.title())}

    def put(self, name):
        # this line of code will only let price to be passed in data
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # or use list comprehension
        # {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
