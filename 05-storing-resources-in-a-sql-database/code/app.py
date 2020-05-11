from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'mee6'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

items = [] # empty list, temporary database for storing data for our API

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
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        # if an item with the given name already exists, we don't have to create any item
        # since all items are unique
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        # if this line is not there python will take items as a local variable
        # and it will be like assigning a variable using that variable itself
        # which will throw an error
        global items
        # modify items list such that all items except name item are in the list
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': '{} deleted'.format(name.title())}

    def put(self, name):
        # this line of code will only let price to be passed in data
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port = 5000, debug = True)
