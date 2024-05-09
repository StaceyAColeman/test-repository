# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 00:28:06 2024

@author: stace
"""
#import sqlite3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from models.item import ItemModel
output_file = open('C:/Users/stace/Development/API 2024/Section5/code/Secondtextfile.txt', 'w')


class Item(Resource):
    print("In Item")
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
            type=float,
            required=True,
            help="This field cannot be left blank!"
            )
    
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id.")
    

    @jwt_required()
    def get(self, name): 
       '''       connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        
        return {'message': "Item not found"}, 404
'''
       item = ItemModel.find_by_name(name)
       if item:
           return item.json()     
       return {'message': "Item not found"}, 404
        
    
    def post(self, name):
        itemfound = ItemModel.find_by_name(name)
        print("itemfoound = ", itemfound)
        if itemfound:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400     
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500
        return item.json(), 201
    

                
    def put(self, name):
        itemfound = ItemModel.find_by_name(name)

        data = Item.parser.parse_args()
#        item = ItemModel(name, data['price'], data['store_id'])

        output_file.write(str(itemfound))
        if itemfound is None:
            try:
               item = ItemModel(name, data['price'], data['store_id'])
            except:
               return {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                item.price = data['price']
            except:
                return {"message": "An error occurred updating the item."}, 500
        item.save_to_db()
#        output_file.close()
#        data = Item.request.get_json()

        return item.json()
  
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

            return {'message':  "item deleted"}
#        print("Name = " , name, "Price = ", data['price'])
#        items.append(item)
        return jsonify({'message': 'item not found'})
class ItemList(Resource):
    def get(self):
  
#        return {'message': "No items found"}, 404
        return {'items': [x.json() for x in ItemModel.query.all()]}
    
#Code appended on 4/20/2024

    def create_store():
        print("Inside create_store")
        request_data = request.get_json()
        new_store = {
            'name': request_data['name'],
            'item':[]
            }
#    stores.append(new_store)
#    return "Hello World"
        return jsonify(new_store)

# GET /store/<string:name>  // Get a store with a given name and return data about it 'http://127.0.0.1:5000/store/some_name' 

def get_store(name):
    # Iterate over stores
    # if the dtotr name matches, return it
    # If none match, return an error message
    # Use a try, block   April 7, 2024
    for store in stores:
        if store['name'] == name:
          return jsonify(store)
    return jsonify({'message': 'store not found'})


# GET /stores                // REturn a list of all the stores

def get_stores():
    return jsonify({'stores': stores})


# POST /store/<string:name>/item {name:, price:}  // Create an item inside a specific store with given name

def create_item_in_store(name):
    print("Inside create_item_in_store", "name = ", name)

    request_data = request.get_json()
    print("request_data",request_data)
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
                }         
        store['items'].append(new_item)    
        return jsonify(store)
# Or    return jsonify('new_item)
    return jsonify({'message': 'store not found'})

# GET /store/<string:name>/item  //Get all the items within a specif store

def get_item_in_store(name):
#    print("inside get_item_in_store")
    for store in stores:
        if store['name'] == name:
          return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'})
