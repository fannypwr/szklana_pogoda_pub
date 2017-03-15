from flask import jsonify, request

from app import db
from app.api import api as api_bl
from app.models import User, load_user


@api_bl.route('/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({'users': [u.to_json() for u in users]}), 200


@api_bl.route('/users/<int:user_id>')
def get_user(user_id):
    user = load_user(user_id)
    if user:
        return jsonify(user.to_json())
    else:
        return jsonify({})


@api_bl.route('/users/', methods=['POST'])
def add_user():
    try:
        user = User.from_json(request.json)
        db.session.add(user)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as ex:
        return jsonify({'error': 'Wrong data provided or db error: {} {}'.format(ex, request.json)})
