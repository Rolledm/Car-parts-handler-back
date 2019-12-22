from flask import Flask, jsonify,request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
table = client.cph.cph

def get_users():
    obj = table.find({})
    users = []
    for iter in obj:
        users.append(f"{iter['name']} \'{iter['nickname']}\'")
    return users

@app.route('/cph/api/v1.0/parts', methods=['GET'])
def get_available_users():
    return jsonify(get_users())

@app.route('/cph/api/v1.0/parts/createUser', methods=['POST'])
def create_user():
    name = request.form.get('name')
    nickname = request.form.get('nickname')
    table.insert_one({'name': name, 'nickname': nickname, 'cars': []})
    return get_available_users()

@app.route('/cph/api/v1.0/parts/removeUser/<string:nickname>', methods=['POST'])
def remove_user(nickname):
    table.remove({'nickname': nickname})
    return get_available_users()

def get_cars(nickname):
    obj = table.find_one({'nickname': nickname})['cars']
    cars = []
    for iter in obj:
        cars.append(f"{iter['name']} \'{iter['codename']}\'")
    return cars

@app.route('/cph/api/v1.0/parts/<string:nickname>', methods=['GET'])
def get_available_cars(nickname):
    return jsonify(get_cars(nickname))

@app.route('/cph/api/v1.0/parts/<string:nickname>/createCar', methods=['POST'])
def create_car(nickname):
    person = table.find_one({'nickname': nickname})
    name = request.form.get('name')
    codename = request.form.get('codename')
    mileage = request.form.get('mileage')
    person['cars'].append({'name': name, 'codename': codename, 'mileage': mileage, 'parts': []})
    table.save(person)
    return get_available_cars(nickname)

@app.route('/cph/api/v1.0/parts/<string:nickname>/removeCar/<string:codename>', methods=['POST'])
def remove_car(nickname, codename):
    person = table.find_one({'nickname': nickname})
    pointer = 0
    for iter in person['cars']:
        if iter['codename'] == codename:
            pointer = iter
            break
    person['cars'].remove(pointer)
    table.save(person)
    return get_available_cars(nickname)

def get_parts(nickname, car):
    obj = table.find_one({'nickname': nickname})['cars']
    car_info = 0
    for iter in obj:
        if iter['codename'] == car:
            car_info = iter
            break
    return car_info

@app.route('/cph/api/v1.0/parts/<string:nickname>/<string:car>', methods=['GET'])
def get_available_parts(nickname, car):
    return jsonify(get_parts(nickname, car))

@app.route('/cph/api/v1.0/parts/<string:nickname>/<string:car>/createPart', methods=['POST'])
def create_part(nickname, car):
    name = request.form.get('name')
    mileage1 = request.form.get('mileage1')
    mileage2 = request.form.get('mileage2')
    obj = table.find_one({'nickname': nickname})
    for iter in obj['cars']:
        if iter['codename'] == car:
            iter['parts'].append({'name': name, 'mileage1': mileage1, 'mileage2': mileage2})
            break
    table.save(obj)
    return get_parts(nickname, car)

@app.route('/cph/api/v1.0/parts/<string:nickname>/<string:car>/removePart/<string:name>', methods=['POST'])
def remove_part(nickname, car, name):
    person = table.find_one({'nickname': nickname})
    pointer = 0
    for iter in person['cars']:
        if iter['codename'] == car:
            for iter1 in iter['parts']:
                if iter1['name'] == name:
                    pointer = iter1
                    break
            iter['parts'].remove(pointer)
            break
            
    table.save(person)
    return get_available_parts(nickname, car)



if __name__ == '__main__':
    app.run(debug=True)