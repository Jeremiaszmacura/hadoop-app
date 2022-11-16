"""Routes related to AdressData database colection."""
from flask import request, jsonify, Response, Blueprint

from flaskr.models.db import db
from flaskr.models.adress_data import AdressData


adress_data_blueprint = Blueprint("adress_data_blueprint", __name__)


@adress_data_blueprint.route("/")
def hello_world() -> str:
    """Test route."""
    return "<p>Hello, World!</p>"


@adress_data_blueprint.route("/test-db")
def test_db() -> str:
    """Test databse connection."""
    colection = db[f"{AdressData.colection_name}"]
    adress_data = AdressData("fasfas", ["fasdf", "fasdf", "fasdf"])
    result = colection.insert_one(adress_data.__dict__)
    colection.delete_one({'_id': result.inserted_id})
    return f"<p>Inserted id: {result.inserted_id}</p>"
