import re
from datetime import date
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login_manager

FORMAT_PROBLEM = 'Problem with date format'
PROVIDE_NAME = 'Name must be provided'
VALUE_TEMP = 'Wrong or incomplete data have been provided'


class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    temperatures = db.relationship('Temperature', backref='place')

    def to_json(self):
        json_format = dict(
            name=self.name,
            temperatures=[t.to_json() for t in self.temperatures])
        return json_format

    @staticmethod
    def from_json(json_place):
        name = json_place.get('name')
        if not name:
            raise ValueError(PROVIDE_NAME)
        return Place(name=name)

    def __repr__(self):
        return '<Place id: {} name: {}>'.format(self.id, self.name)


class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grades = db.Column(db.Integer, nullable=False)
    day = db.Column(db.DATE, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))

    def to_json(self):
        json_format = dict(
            grades=self.grades,
            day=self.day,
            place_id=self.place_id
        )
        return json_format

    @staticmethod
    def from_json(json_temperature):
        grades = json_temperature.get('grades')
        place_id = json_temperature.get('place_id')
        json_date = json_temperature.get('day')
        date_regex = re.compile(r'(\d{4})\W(\d{1,2})\W(\d{1,2})')
        try:
            y, m, d = re.search(date_regex, json_date).groups()
            day = date(year=int(y), month=int(m), day=int(d))
        except AttributeError:
            print(FORMAT_PROBLEM)
            raise
        if not grades or not day or not place_id:
            raise ValueError(VALUE_TEMP)
        return Temperature(grades=grades, day=day, place_id=place_id)

    def __repr__(self):
        return '<Temperature id: {} grades: {} day: {} place {}>'.format(self.id, self.grades, self.day, self.place)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, index=True)
    hashed_pass = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=1)
    active = db.Column(db.Boolean, default=True)

    def verify_password(self, password):
        return check_password_hash(self.hashed_pass, password)

    def to_json(self):
        json_format = dict(
            email=self.email,
            hashed_pass=self.hashed_pass,
            role_id=self.role_id,
            active=self.active
        )
        return json_format


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, index=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

