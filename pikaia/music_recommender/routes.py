import csv

from pikaia import app, db
from pikaia.token import token_required
from pikaia.models.models import Songs, Ratings, User
from flask import request, jsonify

from pandas import read_csv
from scipy.spatial.distance import euclidean


@app.route('/add-music', methods=['POST'])
@token_required
def add_music(current_user):
    # allowing only admin user to perform an action
    if not current_user.admin:
        return jsonify({'message': 'You do not have the permission to perform that function!'})

    try:
        data = request.get_json()
        new_song = Songs(song_name=data['song_name'], song_link=data['song_link'],
                         song_author=data['song_author'],
                         song_cover=data['song_cover'])
        db.session.add(new_song)
        db.session.commit()
        for user in User.query.all():
            new_rating = Ratings(song_id=new_song.id, user_id=user.id, ratings=0)
            db.session.add(new_rating)
            db.session.commit()

    except:
        return jsonify({'message': 'The song exists!'})

    return jsonify({'message': 'New music added!'})


# @app.route('/recommend-music', methods=['GET'])
# @token_required
# def recommend_music(current_user):
#     user = User.query.all()
#     ratings = Ratings.query.all()
#     print(ratings)
#     return jsonify({'musics': "Terminal"})


@app.route('/rating', methods=['PUT'])
@token_required
def user_create_song_rating(current_user):
    # admin users cannot use this route
    if current_user.admin:
        return jsonify({'message': 'This delete route is not for Admin users user route /chat/[user_id]'})

    data = request.get_json()
    new_rating = Ratings(song_id=data['song_id'], user_id=current_user.id, ratings=data['rating'])
    db.session.add(new_rating)
    db.session.commit()
    return jsonify({'message': 'Rating added'})


@app.route('/recommend-music', methods=['PUT'])
@token_required
def recommend_user_song(current_user):
    user_id = current_user.id

    ratings_data = Ratings.query.all()
    user = User.query.all()
    song = Songs.query.all()

    if not ratings_data:
        return jsonify({'message': 'No song found!'})

    user_data = []
    rating_columns = ["user id"]

    for user in user:
        user = [user.id]
        user_data.append(user)

    song_data = 0
    for song in song:
        song_data = song.id
        rating_columns.append(song_data)

    with open('ratings', 'w') as f:
        write = csv.writer(f)
        write.writerow(rating_columns)
        write.writerows(user_data)

    data_url = 'ratings'
    ratings = read_csv(data_url, index_col=0)  # Index_col=0 skips the row numbers
    ratings = ratings.fillna(0)  # Replaces NaN with 0

    user_rating = []
    for rating in ratings_data:
        if rating.song_id == 0:
            user_rating.append(0)
        else:
            user_rating.append([rating.user_id, rating.song_id, rating.ratings])

    song_ratings = []
    k = 0
    for i in range(len(user_rating)):
        song_ratings.append(user_rating[i][2])
        if len(song_ratings) == song_data:
            for j in range(song_data):
                if len(song_ratings) == song_data:
                    k += 1
                    ratings.loc[k] = song_ratings
                song_ratings.pop(0)

    print(ratings)

    def distance(person1, person2):
        distance = euclidean(person1, person2)
        return distance

    def most_similar_to(user_id):
        person = ratings.loc[user_id]
        closest_distance = float('inf')
        closest_person = ''
        for other_person in ratings.itertuples():
            if other_person.Index == user_id:
                # don't compare a person to themself
                continue
            distance_to_other_person = distance(person, ratings.loc[other_person.Index])
            if distance_to_other_person < closest_distance:
                # new high score! save it
                closest_distance = distance_to_other_person
                closest_person = other_person.Index
        return closest_person

    similar_id = most_similar_to(int(user_id))

    output = []
    similar_rating = Ratings.query.filter_by(id=similar_id).all()
    for rating in similar_rating:
        for song in Songs.query.filter_by(song_id=rating.song_id):
            similar_song = {'song_id': song.id, 'song_name': song.song_name, 'song_link': song.song_link}
            output.append(similar_song)

    return jsonify({'similar': output}), 200


@app.route('/song/<id>', methods=['DELETE'])
@token_required
def delete_song(current_user, id):
    # allowing only admin user to perform an action
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    songs = Songs.query.filter_by(id=id).first()
    # no user found
    if not songs:
        return jsonify({'message': 'No song found!'})

    # user found
    db.session.delete(songs)
    db.session.commit()
    return {'message': 'song has been deleted! '}, 200


@app.route('/all-songs', methods=['GET'])
@token_required
def get_all_songs(current_user):
    # allowing only admin user to perform an action
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    # query users table
    songs = Songs.query.all()
    output = []
    for song in songs:
        song_data = {'id': song.id, 'name': song.song_name, 'link': song.song_link}
        output.append(song_data)

    return jsonify({'songs': output}), 200
