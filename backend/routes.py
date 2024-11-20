from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return data, 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for x in data:
        if x.get("id") == id:
            return x,200
    return {"message": "resource not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    request_data = json.loads(request.data)
    for x in data:
        if x.get("id") == request_data.get("id"):
            return {"Message": "picture with id {} already present".format(request_data.get("id"))},302
    data.append(request_data)
    return request_data, 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    request_data = json.loads(request.data)
    for x in range(len(data)):
        if data[x].get("id") == request_data.get("id"):
            data[x] = request_data
            return {"Message": "picture with id {} update sucess".format(request_data.get("id"))},200
    return {"message": "resource not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for x in range(len(data)):
        if data[x].get("id") == id:
            del data[x]
            return {"Message": "picture with id {} delete sucess".format(id)},204
    return {"message": "resource not found"}, 404

