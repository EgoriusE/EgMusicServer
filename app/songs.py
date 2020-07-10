from flask import jsonify

from app import app
from app.auth import token_auth
from app.models import Song


@app.route('/songs/<int:id>', methods=['GET'])
@token_auth.login_required
def get_song(id):
    return jsonify(Song.query.get_or_404(id).to_dict())


@app.route('/songs', methods=['GET'])
@token_auth.login_required
def get_songs():
    data = Song.to_collection_dict()
    return jsonify(data)
