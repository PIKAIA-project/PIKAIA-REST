from pikaia import app, db
from pikaia.token import token_required
from pikaia.models.models import Binaural
from flask import request, jsonify


@app.route('/add-binaural', methods=['POST'])
@token_required
def add_binaural(current_user):
    # allowing only admin user to perform an action
    if not current_user.admin:
        return jsonify({'message': 'You do not have the permission to perform that function!'})

    try:
        data = request.get_json()
        new_beat = Binaural(binaural_name=data['name'],
                            binaural_data=data['data'],
                            binaural_type=data['type'])
        db.session.add(new_beat)
        db.session.commit()

    except:
        return jsonify({'message': 'The Beat exists!'})

    return jsonify({'message': 'New music added!'})


@app.route('/binaural-<type>', methods=['GET'])
@token_required
def add_binaural_by_type(current_user, type):
    # admin users cannot use this route
    if current_user.admin:
        return jsonify({'message': 'This delete route is not for Admin users user route /chat/[user_id]'})

    beats = Binaural.query.all()

    try:
        beat_list = []
        for beat in beats:
            if beat.type == type:
                beat_list.append([beat.name, beat.data])
    except:
        return jsonify({'message': 'No beat type of that requested'})
    return jsonify({'beats': beat_list})
