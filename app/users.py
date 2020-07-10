from app import app, jsonify, request, db
from app.models import User
from app.errors import bad_request
from flask import url_for
from flask import jsonify, g
from app.auth import basic_auth
from app.auth import token_auth


@app.route('/api/')
def index():
    return "Welcome to EgMusicServer!"


@app.route('/users/<string:email>', methods=['GET'])
def get_user(email):
    return jsonify(User.query.get_or_404(email).to_dict())


@app.route('/api/sign_up', methods=['POST'])
def sign_up():
    data = request.get_json() or {}
    if 'name' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include name, email and password fields')
    if User.query.filter_by(name=data['name']).first():
        return bad_request('please use a different name')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('get_user', email=user.email)
    return response


@app.route('/api/sign_in', methods=['POST'])
@basic_auth.login_required
def sign_in():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})


@app.route('/users/<email>', methods=['PUT'])
@token_auth.login_required
def update_user(email):
    user = User.query.get_or_404(email)
    data = request.get_json() or {}
    if 'name' in data and data['name'] != user.name and \
            User.query.filter_by(name=data['name']).first():
        return bad_request('please use a different name')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())


@app.route('/api/sign_in', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
