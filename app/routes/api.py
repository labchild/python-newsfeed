from flask import Blueprint, request, jsonify, session
import sys
from app.models import User
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
    # get data from request obj
    data = request.get_json()

    # access db
    db = get_db()

    # attempt to create a new user
    try:
        newUser = User(
            username = data['username'],
            email = data['email'],
            password = data['password']
        )

        # save new user in db
        db.add(newUser)
        db.commit()
    except:
        # insert failed, so rollback and send error to frontend
        print(sys.exe_info()[0])
        db.rollback()
        return jsonify(message = 'Signup failed'), 500

    session.clear()
    session['user_id'] = newUser.id
    session['loggedIn'] = True

    return jsonify(id = newUser.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
    # remove session variables
    session.clear()
    return '', 204

@bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()

    # look for username in db
    try:
        user = db.query(User).filter(User.email == data['email']).one()
    except:
        print(sys.exc_info()[0])

        return jsonify(message = 'Incorrect credentials'), 400
    
    # check password given against user's password from db
    if user.verify_password(data['password']) == False:
        return jsonify(message = 'Incorrect credentials'), 400
    
    # create logged in session
    session.clear()
    session['user_id'] = user.id
    session['loggedIn'] = True

    return jsonify(id = user.id)