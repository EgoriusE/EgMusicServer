from flask import jsonify

from app import app
from app.auth import token_auth
from app.models import Album


@app.route('/albums/<int:id>', methods=['GET'])
@token_auth.login_required
def get_album(id):
    return jsonify(Album.query.get_or_404(id).to_dict())


@app.route('/albums', methods=['GET'])
@token_auth.login_required
def get_albums():
    data = Album.to_collection_dict()
    return jsonify(data)
