import sys
from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
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


  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True
    
  return jsonify(id = newUser.id) # includes id of newUser

@bp.route('/users/logout', methods=['POST'])
def logout():
  # remove session variables
  session.clear()
  return '', 204 

@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()
  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    print(sys.exc_info()[0])
  if user.verify_password(data['password']) == False:
    return jsonify(message = 'Incorrect credentials'), 400

  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True
  
  return jsonify(id = user.id)

@bp.route('/comments', methods=['POST']) #First step of connecting to db
def comment():
  data = request.get_json()
  db = get_db()
  try:
  # create a new comment
    newComment = Comment(
    comment_text = data['comment_text'],
    post_id = data['post_id'],
    user_id = session.get('user_id')
  )

    db.add(newComment) # preps db for inserting
    db.commit() # officially adds to db
  except:
    print(sys.exc_info()[0])

    db.rollback() # discards pending commit if it fails
    return jsonify(message = 'Comment failed'), 500
  
  return jsonify(id = newComment.id)