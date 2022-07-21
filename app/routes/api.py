from flask import Blueprint, request, jsonify
from app.models import User
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()

  # create a new user
  newUser = User(
    username = data['username'],    # js version would look like 'username = data.username,
    email = data['email'],          #                            'email = data.email,
    password = data['password']     #                            'password = data.password
  )

  # save in database
  db.add(newUser) # preps db to insert newUser into database
  db.commit()

  return jsonify(id = newUser.id) # includes id of newUser 