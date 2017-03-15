from flask import jsonify, request

from app import db
from app.api import api as api_bl
from app.models import Place


BAD_DATA = 'bad data'


@api_bl.route('/places/')
def get_places():
    places = Place.query.all()
    return jsonify({'places': [p.to_json() for p in places]})


@api_bl.route('/places/<int:place_id>')
def get_place(place_id):
    place = Place.query.filter_by(id=place_id).first()
    if place:
        return jsonify(place.to_json())
    return jsonify({})


@api_bl.route('/places/', methods=['POST'])
def add_place():
    try:
        place = Place.from_json(request.json)
    except Exception as ex:
        print(ex)
        return jsonify({}), 400
    try:
        db.session.add(place)
        db.session.commit()
        return jsonify(place.to_json()), 201
    except Exception as ex:
        print(ex)
        return jsonify({'error': BAD_DATA}), 400
