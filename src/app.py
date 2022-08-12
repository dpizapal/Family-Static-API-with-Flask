"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#GET members-----------------
@app.route('/members', methods=['GET'])
def handle_hello():

    members = jackson_family.get_all_members()
    
    response_body = {
        "hello": "world",
        "family": members
    }

    if members:
        return jsonify(members), 200
    else:
        return jsonify(members), 400

#GET member-----------------
@app.route("/member/<int:member_id>", methods=["GET"])
def get_member(member_id):
    return jsonify(jackson_family.get_member(member_id)), 200


#POST-------------------
@app.route("/member", methods=["POST"])
def add_member():
    member = {
        "first_name": request.json.get("first_name"),
        "age": request.json.get("age"),
        "lucky_numbers": request.json.get("lucky_numbers"),
        "id": request.json.get("id")
    }

    status = jackson_family.add_member(member)

    if status:
        return jsonify(member), 200
    else:
        return jsonify("Member is not added"), 400

#DELETE-------------------
@app.route("/member/<int:member_id>", methods = ["DELETE"])
def kick_member(member_id):

    status = jackson_family.delete_member(member_id)

    if status:
        return jsonify({"done": True}), 200
    else:
        return jsonify("Member doesn't exists"), 400



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)