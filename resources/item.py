# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 22:48:29 2025

@author: stace
"""
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.item import ItemModel

class Item(Resource):
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
        item = ItemModel.find_by_name(name)
#        return print("What the hell?")
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    
      def post(self, name):
#           finder = ItemModel.find_by_name(name)
#           print("finder = ", finder)
   
           if ItemModel.find_by_name(name):
                return {"message": "A item with that name already exists."}, 400                  
            
           data = Item.parser.parse_args()       
           
           item = ItemModel(name, data['price'], data['store_id'])
#           result = ItemModel.insert(item)
#           print(result)
           try:
              item.save_to_db()
           except:
               return {"message": "An error occurred inserting the item."}, 500
#           print("Made it this far...")
           return item.json(), 201
    
            
      def delete(self, name):
          item = ItemModel.find_by_name(name)
          if item:
              item.delete_from_db()
              
          return {'message': 'Item deleted'}
          
       
      def put(self, name):               
          data = Item.parser.parse_args()

          item = ItemModel.find_by_name(name)
#          print("item = ", item)
          
#          updated_item = ItemModel(name, data['price'])
          
          if item is None:
              item = ItemModel(name, data['price'], data['store_id'])
#              try: 
#                 updated_item.insert()        
#              except:
#                  return {"message": "An error occurred inserting the item."}, 500
          else:
              item.price = data['price']
#              try:
#                 updated_item.update()
#              except:
#                  return {"message": "An error occurred updating the item."}, 500              
          item.save_to_db()
          
          return item.json()   
                
class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
