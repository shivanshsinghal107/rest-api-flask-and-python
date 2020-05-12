# Rest-API-Flask-and-Python

## HTTPS Verbs (as if we're at the server end):
- **POST** - to give data to the server & create it if its new or fail if it already exists<br>
- **GET** - to retrieve requested data from the server database & send it to the user<br>
- **PUT** - to give data to the server & then do one of two things, either create it if its new or modify it if it already exists<br>
- **DELETE** - to remove requested data from the server database

As a web server a POST request means to receive data from the user & a GET request means to sent back the data to the user.<br>
However for browser these things become opposite i.e. for a browser a POST request means sending data to the server and a GET request means to receive the requested data from the server.

**What json is?**<br>
Basically JSON is a set of key value pairs like a dictionary. However JSON is not a dictionary, it is a long string. **JSON always uses double quotes to represent the data**.

**jsonify() method:**<br>
To retrieve the requested data there should be some sort of a way to convert the python list to some kind of string which we could send back to the internet.<br>
Fortunately, flask helps us out here. It has a method called `jsonify` which takes in **dictionary** and sends back JSON.<br>
```python
stores = [
  {
     'name': 'The Indian',
     'items': [
         {
           'name': 'first',
           'price': 170
         }
     ]
  }
]

@app.route('/stores')
def get_stores():
    return jsonify(stores)
```

But here `jsonify(stores)` would not work because stores is not a dictionary, its a list. So what should we do?<br>
Don't think much, Simply pass the list as dictionary:
```python
return jsonify({'stores': stores})
```

***This method always return a dictionary not a list.***

*If we're using <b>flask restful</b> then we just have to return dictionary without needing the jsonify method i.e. flask restful automatically converts dictionary into JSON, isn't that cool.*

http://127.0.0.1:5000/store<br>
Lets break this down:<br>
- *127.0.0.1* is our **Local Computer**.<br>
- *5000* is the **PORT** that we are running on.<br>
- */store* is the **Endpoint** we're accessing.

**APIs**: The APIs works with resources and resource should be a class.

**OBJECTS & CLASSES IN PYTHON**:<br>
- A *class* is a type of abstract data type consisting of various data with different methods performed on that data, whereas an *object* is simply a class defined for some specific data passed as parameters into the class(like a variable of data type class).<br>
- **self**: Whenever we write object dot method(i.e. when any method is called on any object), always self gets passed in(i.e. by default/automatically) as an argument. That's why we need to pass self as an argument in every method of a *class*.<br>
- **@classmethod**: However we can tell python that we do not need the self to be passed in, so just before the line defining the method put `@classmethod` which will take `cls`(the *class* itself) as an argument instead of self.<br>
So whenever we call `@classmethod` what we pass is not the *object* but the *class*.<br>
- **@staticmethod**: And if we do not want a single argument to be passed in our method, then we use `@staticmethod` which takes no argument for a method defined as static.<br>
Hence now we can directly write `class.method`, not necessarily `object.method`.

Now very common question that comes to mind is:<br>
**Why would I want to use @classmethod or @staticmethod?**<br>

**Why is PUT called an idempotent request?**<br>
PUT is known as an idempotent request, because even if the thing that you are doing with this request has already happened, you can still do the request again & it won't fail.<br>

**What's the most popular HTTP status code?**<br>
!(404) i.e. 200

### HTTP Status codes & their meanings:
- **200 OK** - when the server returns some data & say everything's OK, I have given you what you wanted
- **404 NOT FOUND** - it shows when the server does not find what the client requested
- **201 CREATED** - it shows when the object has been created & added to the database
- **202** - it is similar to 201 which is accepted when you're delaying the creation of an object, it may fail to actually add the object to the database but that's out of client's control
- **400 BAD REQUEST** - it is shown when POST request fails i.e. the data given by user already exists. This is known as a Bad request & its not our application's fault, its client's fault because they made a request with an invalid data(its invalid because its already in the server)
- **401 UNAUTHORIZED** - it is shown when GET request fails i.e. the client is not authorized to send the request to the server
- **500 INTERNAL SERVER ERROR** - it occurs when something wents wrong on the server side i.e. its not client's fault

*Using the right status codes is very important as it is a very quick way for client's like mobile applications or web applications to check whether things gone right or not.*

**get_json() method:**<br>
Whenever anyone(like Postman) makes a request, that request is going to have a JSON payload & body attached to it.<br>
If the request does not attach a JSON payload or if proper Content-type header(i.e. application/json) is not set then `data = request.get_json()` will throw an error.

In case we are not sure that our client is going to give JSON or not, we can prevent this from giving an error by two things that we can pass in this method:<br>
- `data = request.get_json(force = True)`: This method means that you do not need the Content-type header, it will look in the content & it will format it even if the Content-type header is not set(application/json). But always using this will mean just processing the text even if its not correct.
- `data = request.get_json(silent = True)`: This method doesn't do anything, just returns null when the request does not attach a JSON payload or if proper Content-type header is not set.

**filter function:**<br>
filter function takes two arguments:
1) filtering logic or filtering basis
2) list of items of which filtering is to be done

The filter function returns a filter object, and on a filter object we can call a couple of functions:<br>

- `list(filter(lambda x: x['name'] == name, items))`: will return a list of items satisfying the filter condition.
- `next(filter(lambda x: x['name'] == name, items))`: will return the first item from the list of items satisfying the filter condition.

Here we can call next again we if we want second item & again if third item and so on.<br>
Also if the next function doesn't find any items then it will give an error, so to avoid that we can write -<br>
`next(filter(lambda x: x['name'] == name, items), None)` which will simply return None if no items are found.

**JWT** stands for **JSON Web Token**. It is used to encrypt data.

**Resource**: Esentially a resource is what an API thinks of.
**What is a model & a resource?**<br>
A Model is internal representation of an entity whereas the resource is an external representation of the entity.<br>
Our API clients like a website or a mobile app think they are interacting with resources & when our API responds, it responds with resources. However when we deal internally in our code with a user, we are actually using a model.<br>
So a model is a helper that allows us to interact with the user or give more flexibility to our program without polluting the resource which is what the client interact with.

**SSL(Secure Sockets Layer)**:
SSL allows communication between the client and the server to be encrypted.
