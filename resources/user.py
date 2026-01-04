# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 03:45:31 2023

@author: stace
"""
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    def post(self):
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that user name already exists."}, 400
        
        user = UserModel(**data)
        user.save_to_db()
        
        return {"message": "User created successfully."}, 201
        