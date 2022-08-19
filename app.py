from flask import Flask, json
from flask import jsonify, request
from flask.wrappers import Response
import pymongo
from pymongo.common import SERVER_SELECTION_TIMEOUT
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from werkzeug.wrappers import response

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
            host="localhost",
            port=27017,
            serverSelectionTimeoutMS = 1000
        )
    db = mongo.company
    mongo.server_info()
except:
    print("ERROR - no db")


    
#CREATE

@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = {
            "name":request.form["name"], 
            "email":request.form["email"],
            "password":request.form["password"]
         }
        dbResponse = db.users.insert_one(user)
        #print(dbResponse.inserted_id)

        return Response(
                response=json.dumps(
                {"message":"user created", 
                 "id":f"{dbResponse.inserted_id}"
                }  
             ),status=200,
            mimetype="application/json"
            )
            
    except Exception as ex:
        print(ex)



#READ

@app.route("/users", methods=["GET"])
def user_data():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
          response=json.dumps(data),
          status=500,
          mimetype="application/json"
            
          )
    except Exception as ex:
        print(ex)
        return response(
            response=json.dumps(
            {
                "message":"cannot read users"
             }    
            ),
        status = 500,
        mimetype="application/json"
        )



#UPDATE

@app.route("/users/<id>", methods = ["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
                {"_id":ObjectId(id)},
                {"$set":{"name":request.form["name"], "email":request.form["email"] ,"password":request.form["password"]}}
                
            )
        if dbResponse.modified_count == 1:
             return Response (
                 response=json.dumps(
            {
                "message":"user data updated"
             }    
            ),
        status = 200,
        mimetype="application/json"
        )
        else:
            return Response (
                 response=json.dumps(
            {
                "message":"no new data to update or user not found"
             }    
            ),
        status = 200,
        mimetype="application/json"
        )
        
    except Exception as ex:
        print(ex)
        return response(
            response=json.dumps(
            {
                "message":"user data couldn't be updated"
             }    
            ),
        status = 500,
        mimetype="application/json"
        )




#DELETE

@app.route("/users/<id>", methods = ["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id":ObjectId(id)})

        if dbResponse.deleted_count == 1:
            return Response(
            response=json.dumps(
            {
                "message":"user data deleted", "id":f"{id}"
             }    
            ),
        status = 300,
        mimetype="application/json"
        )
        else:
            return Response(
            response=json.dumps(
            {
                "message":"user not found"
             }    
            ),
        status = 300,
        mimetype="application/json"
        )
        
        
    except Exception as ex:
        print(ex)
        return response(
            response=json.dumps(
            {
                "message":"user data couldn't be deleted"
             }    
            ),
        status = 500,
        mimetype="application/json"
        )

if __name__ == "__main__":
    app.run(debug=True)
