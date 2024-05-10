from werkzeug.security import safe_str_cmp
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

from security import authenticate, identity
from resources.user import UserRegister
from models.user import UserModel
from resources.item import Item, ItemList
from resources.store import Store, StoreList



output_file = open('C:/Users/stace/Development/API 2024/Section5/code/firsttextfile.txt', 'w')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = 'jose'
 
    

#app.secret_key = 'jose'

api = Api(app)

parser = reqparse.RequestParser()    
parser.add_argument(app, authenticate, identity)
#parser.add_argument(identity)
#output_file.write(str(parser))
args = parser


#jwt = JWTManager(app, authenticate, identity) #Endpoint http://127.0.0.1:5000/auth
jwt = JWTManager(app, add_context_processor=True )

print("jwt =", jwt)
#@app.route("/auth")

class Auth(Resource):
    print("In Auth")
    @app.route("/auth", endpoint='getAuth')
    @jwt_required()
    def getAuth():   
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200

    @app.route("/auth", methods=["POST"], endpoint='postAuth')
#    print("in Post")

    def postAuth():
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        user = UserModel.find_by_username(username)
        output_file.write(str(user))
        print("user = ", username)
        if user and safe_str_cmp(user.password, password):
            access_token = create_access_token(identity=username)
 #           return {'message': "An item with name'{}' already exists.".format(user)}, 400
 #       if username != user[1] or password != user[2]:
 #          return jsonify({"msg": "Bad username or password"}), 401
        
#        return jsonify(user)
            output_file.close
            return jsonify(access_token=access_token)
        return jsonify({"msg": "Bad username or password"}), 401
        # data = request.get_json(force=True) or getjson(silent=True)

    

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/items/<string:name>')     # http://127.0.0.1:5000/student/Rolf
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)