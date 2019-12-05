import uuid
from haversine import haversine, Unit
from flask import Flask
from flask import request
from flask import jsonify
import requests
import json


app = Flask(__name__)


import  MySQLdb
db = MySQLdb.connect(host="mysql",user="shipping",
              passwd="secret",db="cities")

CART_URL = "http://cart:8080/shipping/"

@app.route('/codes', methods=['GET'])
def codes():
    query = "select code, name from codes order by name asc;"
    c = db.cursor()
    c.execute(query)
    records = c.fetchall()
    c.close()

    response = []
    for record in records:
        response.append({'code': record[0], 'name': record[1]})


    return jsonify(response)


@app.route('/cities/<code>', methods=['GET'])
def cities(code):

    query = "select uuid, name from cities where country_code = '{}';".format(code) 

    c = db.cursor()
    c.execute(query)
    records = c.fetchall()
    c.close()

    response = []
    for record in records:
        response.append({'uuid': record[0], 'name': record[1]})

    return jsonify(response)


@app.route('/calc/<uuid>', methods=['GET'])
def calc(uuid):

    query = "select latitude, longitude from cities where uuid = {}".format(uuid)

    c = db.cursor()
    c.execute(query)
    row = c.fetchone()
    c.close()

    distance_km = 0
    try:
        latitude = row[0]
        longitude = row[1]

        location = (latitude, longitude)
        targetLocation = (51.164896, 7.068792)

        distance_km = haversine(location, targetLocation)

    except:
        return jsonify({'message': 'Error in fetching location'}), 400

    cost = (distance_km * 5)/100
    
    return jsonify({'distance': distance_km, 'cost': cost})


def addToCart(id, data):

    print (CART_URL+str(id))
    response = requests.post(CART_URL+str(id), data=data)
    if response.status_code == 200:
        return response.json()
    else:
        print ("*** Error from cart service: ", response.status_code, response.text)
        return {}

@app.route('/confirm/<id>', methods=['POST'])
def confirm(id):

    print (request.data)
    cart = addToCart(id, request.get_json())
    if not cart:
        return cart, 404
    else:
        return cart

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
