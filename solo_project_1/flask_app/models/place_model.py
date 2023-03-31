from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, session
from flask import flash
from flask_app.controllers import users_controller
from .user_model import User


class Place:
    db = 'foodie_db'
    def __init__(self , data):
        self.id = data['id']
        self.name = data['name']
        self.city = data['city']
        self.cuisine = data['cuisine']
        self.address = data['address']
        self.days = data['days']
        self.opening_time = data['opening_time']
        self.closing_time = data['closing_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.posted_by = None

    @classmethod
    def get_one_w_user(cls, place_id):
        query = 'SELECT * FROM places LEFT JOIN users ON places.user_id = users.id WHERE places.id  = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, {'id': place_id})
        print(results)
        place = cls(results[0])
        place.posted_by = results[0]['first_name']
        print(place.posted_by)
        return results

    @classmethod
    def save(cls,data):
        query = "INSERT INTO places (name,city,cuisine,address, days, opening_time, closing_time, user_id) VALUES(%(name)s,%(city)s,%(cuisine)s, %(address)s, %(days)s, %(opening_time)s, %(closing_time)s, %(user_id)s);"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

    @classmethod
    def get_one(cls, user_id):
        query = 'SELECT * FROM places WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, {'id': user_id})
        print(results[0])
        place = cls(results[0])
        return place
    
    @classmethod
    def update(cls,data):
        query = "UPDATE places SET name = %(name)s, city= %(city)s, cuisine= %(cuisine)s WHERE id = %(id)s;"

        results = connectToMySQL(cls.db).query_db(query,data)

        return results

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM places;'
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        places = []
        for p in results:
            places.append(cls(p))
        print(places)
        return places
    
    @classmethod
    def delete(cls,id): 
        query = "DELETE FROM places WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, {'id': id })
