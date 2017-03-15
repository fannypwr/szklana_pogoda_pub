from flask import jsonify, request
from app import db
from app.api import api as api_bl
from app.models import Temperature


@api_bl.route('/temperatures/places/<int:place_id>')
def get_temperatures(place_id):
    if place_id:
        temperatures = Temperature.query.filter_by(place_id=place_id)
    else:
        temperatures = Temperature.query.all()
    return jsonify({'temperatures': [t.to_json() for t in temperatures]})


@api_bl.route('/temperatures/<int:temp_id>')
def get_temperature(temp_id):
    temperature = Temperature.query.filter_by(id=temp_id).first()
    return jsonify(temperature.to_json())


@api_bl.route('/temperatures/', methods=['POST'])
def add_temperature():
    temperature = Temperature.from_json(request.json)
    db.session.add(temperature)
    db.session.commit()
    return jsonify(temperature.to_json()), 201