from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
  {
     'name': 'The Indian',
     'items': [
         {
           'name': 'first',
           'price': 20
         }
     ]
  }
]

#POST /store {name}
@app.route('/store', methods = ['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
       'name': request_data['name'],
       'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

#GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    # iterate over stores
    for store in stores:
        # if the store name matches return it
        if store['name'] == name:
            return jsonify(store)
    # if none match, return error message
    return jsonify({'message': 'No such store found'})

#GET /stores
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})

#POST /store/<string:name>/item
@app.route('/store/<string:name>/item', methods = ['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'No such item found for the store'})

#GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    # iterate over stores
    for store in stores:
        # if item name matches return it
        if store['name'] == name:
            return jsonify({'items': store['items']})
    # if none match, return error message
    return jsonify({'message': 'No such store found'})
