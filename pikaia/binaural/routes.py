from pikaia import app, db
from pikaia.token import token_required
from pikaia.models.models import Binaural
from flask import request, jsonify, render_template, Response


@app.route('/binaural')
@token_required
def binaural(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    return render_template('add_beats.html')


@app.route('/add-binaural', methods=['POST'])
@token_required
def add_binaural(current_user):
    # allowing only admin user to perform an action
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    try:
        file = request.files['inputFile']
        file_name = request.form['inputFileName']
        file_type = request.form['inputFileType']
        new_beat = Binaural(name=file_name, data=file.read(), type=file_type)
        db.session.add(new_beat)
        db.session.commit()
    except:
        return jsonify({'message': 'Oops! something went wrong'})

    return jsonify({'message': 'New music added!'})


@app.route('/binaural/<beat_type>', methods=['GET'])
@token_required
def get_beats(current_user, beat_type):
    # admin users cannot use this route

    beats = Binaural.query.all()
    beat_list = []
    try:
        for beat in beats:
            if beat.type == beat_type:
                beat_data = beat.data
                beat_list.append(beat_data)
    except:
        return jsonify({'message': 'No beat type of that requested'})
    return Response(beat_list), 200


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
        beat_data = {'id': beat.id, 'name': beat.name}
        output.append(beat_data)

    return jsonify({'users': output}), 200
