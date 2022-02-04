from flask import Flask, make_response, jsonify,request
from flask_mongoengine import MongoEngine
from pymongo import MongoClient
from bson.json_util import dumps
from bson.errors import InvalidId
from bson.objectid import ObjectId




app = Flask(__name__)
#Connect to MongoDB database
mongo_client = MongoClient('mongodb://localhost:27017')

#Access to Database
db = mongo_client.test
#Access to Document
col = db["movie"]

#Object Document Mapper with MongoDB
db = MongoEngine()
db.init_app(app)

#Create Class Movie to create document
class Movie(db.Document):
    _id= db.StringField()
    name = db.StringField()
    description = db.StringField()
    #Convert Document to Json
    def to_json(self):
        return {
            "_id": str(self.pk),
            "name": self.name,
            "description": self.description
            }
#This method for add Movie
@app.route('/api', methods=['POST'])
def db_populate():
    content = request.json
    _name=content['name']
    _desc = content['description']
    if _desc and _name:
        movie = Movie(name=_name,description=_desc)
        movie.save()   
        return make_response("Movie added successfully",201)
    else:
        return not_found()

#Error Handler URL
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status' : 404,
        'message' : 'Not Found' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.route('/api/allmovie', methods=['GET'])
def Read_movies():
    return make_response(dumps(col.find()),200)

#Get movie by ID if it exists, or returns all movies if it doesn't
@app.route('/api/movie/<id>', methods=['GET'])
def Movies(id):
    if not id:
        return False
    try:
        return make_response(dumps(col.find( {'_id':ObjectId(id)} ).limit(1)),200)
    except (InvalidId, TypeError):
        return make_response(dumps(col.find()),200) 

#this method for Delete movie By Id
@app.route('/api/movie/<id>', methods=['DELETE'])
def Delete_ovie(id):
    col.find_one_and_delete( {'_id':ObjectId(id)} )
    return make_response("Movie Delete successfully",201)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")