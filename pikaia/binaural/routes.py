from pikaia import app, db
from pikaia.token import token_required
from pikaia.models.models import Binaural
from flask import request, jsonify, render_template, Response


@app.route('/add-binaural', methods=['POST'])
@token_required
def add_binaural(current_user):
    # allowing only admin user to perform an action
    if not current_user.admin:
        return jsonify({'message': 'You do not have the permission to perform that function!'})

    try:
        data = request.get_json()
        new_binaural = Binaural(binaural_name=data['binaural_name'], binaural_link=data['binaural_link'],
                                binaural_author=data['binaural_author'],
                                binaural_cover=data['binaural_cover'], binaural_type=data['binaural_type'])
        db.session.add(new_binaural)
        db.session.commit()

    except:
        return jsonify({'message': 'The song exists!'})

    return jsonify({'message': 'New beat added!'})


@app.route('/binaural/<beat_type>', methods=['GET'])
@token_required
def get_beats(current_user, beat_type):
    # admin users cannot use this route

    beats = Binaural.query.all()
    beat_list = []
    try:
        for beat in beats:
            if beat.type == beat_type:
                beat_data = {'id': beat.id, 'name': beat.binaural_name, 'link': beat.binaural_link, 'type': beat.type}
                beat_list.append(beat_data)
    except:
        return jsonify({'message': 'No beat type of that requested'})
    return jsonify({'beat': beat_list}), 200


# delete beat
@app.route('/beat/<id>', methods=['DELETE'])
@token_required
def delete_beat(current_user, id):
    # allowing only admin user to perform an action
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    binaural = Binaural.query.filter_by(id=id).first()
    # no user found
    if not binaural:
        return jsonify({'message': 'No beats found!'})

    # user found
    db.session.delete(binaural)
    db.session.commit()
    return {'message': 'beat has been deleted! '}, 200


@app.route('/all-beats', methods=['GET'])
@token_required
def get_all_beats(current_user):
    # allowing only admin user to perform an action
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    # query users table
    beats = Binaural.query.all()
    output = []
    for beat in beats:
        beat_data = {'id': beat.id, 'name': beat.binaural_name, 'link': beat.binaural_link, 'type': beat.type}
        output.append(beat_data)

    return jsonify({'beats': output}), 200
