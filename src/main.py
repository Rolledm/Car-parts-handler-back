from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
table = client.cph.cph
driver = 'rolledm'
car = 'rolledm_car'

@app.route('/cph/api/v1.0/parts/', methods=['GET'])
def get_users():
    obj = table.find({})
    users = []
    for iter in obj:
        users.append(f"{iter['name']} \'{iter['nickname']}\'")
    return jsonify(users)

@app.route('/cph/api/v1.0/parts/<string:nickname>', methods=['GET'])
def get_cars(nickname):
    obj = table.find_one({'nickname': nickname})['cars']
    cars = []
    for iter in obj:
        cars.append(f"{iter['name']} \'{iter['codename']}\'")
    return jsonify(cars)

@app.route('/cph/api/v1.0/parts/<string:nickname>/<string:car>', methods=['GET'])
def get_parts(nickname, car):
    obj = table.find_one({'nickname': nickname})['cars']
    car_info = 0
    for iter in obj:
        if iter['codename'] == car:
            car_info = iter
            break
    return jsonify(car_info)


if __name__ == '__main__':
    app.run(debug=True)