from flask import jsonify

from app import app
from app.auth import token_auth
from app.models import Artist, Group, groups_table


@app.route('/artists/<string:name>', methods=['GET'])
@token_auth.login_required
def get_artist(name):
    return jsonify(Artist.query.get_or_404(name).to_dict())


@app.route('/artists', methods=['GET'])
@token_auth.login_required
def get_artists():
    data = Artist.to_collection_dict()
    return jsonify(data)


@app.route('/groups/<string:name>', methods=['GET'])
@token_auth.login_required
def get_group(name):
    return jsonify(Group.query.get_or_404(name).to_dict())


@app.route('/groups', methods=['GET'])
@token_auth.login_required
def get_groups():
    data = Group.to_collection_dict()
    return jsonify(data)


# @app.route('/group_songs/<string:name>', methods=['GET'])
# @token_auth.login_required
# def get_song_group(name):
#     resources = Group.query.join(groups_table, groups_table.c.creator == Group.name).all()
#     data = {
#         'items': [item.to_dict() for item in resources.items]
#     }
#     return jsonify(data)
