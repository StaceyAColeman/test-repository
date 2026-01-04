# -*- coding: utf-8 -*-
"""
Created on Sat Jan  3 11:29:24 2026

@author: stace
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 22:48:29 2025

@author: stace
"""
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.store import StoreModel

class Store(Resource):
      parser = reqparse.RequestParser()
      parser.add_argument('price',
                           type=float,
                           required=True,
                           help="This field cannot be left blank1"
      )
      parser.add_argument('store_id',
                           type=int,
                           required=True,
                           help="Every item needs a store id."
      )
      @jwt_required
      def get(self, name):
        store = StoreModel.find_by_name(name)
#        return print("What the hell?")
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    
      def post(self, name):
#           finder = ItemModel.find_by_name(name)
#           print("finder = ", finder)
   
           if StoreModel.find_by_name(name):
                return {"message": "A store with that name already exists."}, 400                  
                   
           store = StoreModel(name)

           try:
              store.save_to_db()
           except:
               return {"message": "An error occurred while creating the store."}, 500

           return store.json(), 201
    
            
      def delete(self, name):
          store = StoreModel.find_by_name(name)
          if store:
              store.delete_from_db()
              
          return {'message': 'Store deleted'}
          
       
      def put(self, name):               
          store = StoreModel.find_by_name(name)
#          print("item = ", item)
          
#          updated_item = ItemModel(name, data['price'])
          
          if store is None:
              store = StoreModel(name)
              try: 
                 store.save_to_db()        
              except:
                  return {"message": "An error occurred inserting the store."}, 500
#          else:
#              item.price = data['price']
#              try:
#                 updated_item.update()
#              except:
#                  return {"message": "An error occurred updating the item."}, 500              
#          store.save_to_db()
          
          return store.json()   
                
class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
