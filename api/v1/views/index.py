#!/usr/bin/python3
"""BnB clone index file"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models.review import Review
from models.user import User
from models.state import State


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    class_list = {
        "User": "users",
        "City": "cities",
        "Amenity": "amenities",
        "Review": "reviews",
        "Place": "places",
        "State": "states",
    }
    cl_list = ["User", "City", "Amenity", "Place", "State", "Review"]
    count_dict = {}

    for class_name in class_list.keys():
        count_dict[class_list[class_name]] = storage.count(class_name)

    return jsonify(count_dict)
