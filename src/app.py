from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId


# DataBase Connection with Flas_PyMongo Client
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://brian:123@cluster0-fpdvj.mongodb.net/flask-crud-api?retryWrites=true&w=majority"
mongo = PyMongo(app)


""" Ruoutes for our CRUD-API """


#Ruta PETICIONES GET VER LISTADO SIMPLE DE TODOS LOS DATOS
#  Ruta para poder listar los datos: en la misma ruta de user pero a traves de un metodo diferente
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='aplication/json')


# PEDIR UN OBJETO CON TODOS LOS DATOS relacionados a un Id...
# Creamos una ruta o una consulta dedicada a ese tipo de peticiones
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    print(id)
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")




# Ruta Deleted para ELIMINAR USUARIOS...
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    print(id)
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + 'was deleted successfully'})
    return response




# Ruta para ACTUALIZAR TODOS LOS DATOS!
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    print(id)
    print(request.json)
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username  and email and password:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {
            'username': username,
            'password': hashed_password,
            'email': email
        }})
        response = jsonify({'message': 'User' + id + 'user was updated succesfully!'})
        return response


# Ruta para ACTUALIZAR UN DATO EN ESPECIFICO!
# @app.route('/users/<id>', methods=['PATCH'])





# Ruta CREAR UN OBJETO O USUARIO metodo POST  
@app.route('/users', methods=['POST'])
def create_user():
    # Receiving data
    """ print(request.json)"""
    print(request.json)
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and email and password:
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert(
            {'username': username, 'email': email, 'password': hashed_password}
        )
        response = {
            'id': str(id),
            'username': username,
            'password': hashed_password,
            'email': email
        }
        return response
    else:
        return not_found()

    return {'message': 'received'}




# Ruta envio de CODIGOS DE ESTADO cuando algo sale mal desde servidor...
# Routa manejador de errores o codigod de estado para Errores... Handler = Para enviar codigos de estado como: 404, 202, 500...
@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource Not Found: ' + request.url,
        'status': 404
    })
    response.status_code  = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)