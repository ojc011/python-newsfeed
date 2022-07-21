import sys
from flask import Blueprint, request, jsonify
from app.models import User
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()

  try:
    # create a new user
    newUser = User(
        username = data['username'],    # js version would look like 'username = data.username,
        email = data['email'],          #                            'email = data.email,
        password = data['password']     #                            'password = data.password
    )

    # save in database
    db.add(newUser) # preps db to insert newUser into database
    db.commit()
  except: #insert of data failed, error will be sent to frontend
    print(sys.exc_info()[0])
    
    db.rollback()
    return jsonify(message = 'Signup has failed'), 500

  return jsonify(id = newUser.id) # includes id of newUser 