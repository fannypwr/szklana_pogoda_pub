from flask import jsonify, request

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

