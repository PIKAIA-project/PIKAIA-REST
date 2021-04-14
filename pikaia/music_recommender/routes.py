import csv

from pikaia import app, db
from pikaia.token import token_required
from pikaia.models.models import Songs, Ratings, User
from flask import request, jsonify

from pandas import read_csv, DataFrame
from math import sqrt
from scipy.spatial.distance import euclidean, cosine


@app.route('/add-music', methods=['POST'])
@token_required
def add_music(current_user):
    # allowing only admin user to perform an action
    if not current_user.admin:
        return jsonify({'message': 'You do not have the permission to perform that function!'})

    try:
        data = request.get_json()
        new_song = Songs(song_user_id=data['song_user_id'], song_link=data['song_link'],
                         song_author=data['song_author'],
                         song_cover=data['song_cover'])
        db.session.add(new_song)
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


@app.route('/rating', methods=['POST'])
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


@app.route('/recommend-music/<user_id>', methods=['GET'])
@token_required
def recommend_user_song(current_user, user_id):
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

    for song in song:
        song_data = song.id
        rating_columns.append(song_data)

    with open('ratings', 'w') as f:
        write = csv.writer(f)
        write.writerow(rating_columns)
        write.writerows(user_data)

    data_url = 'ratings'
    ratings = read_csv(data_url, index_col=0)  # Index_col=0 skips the row numbers

    user_rating = []
    for rating in ratings_data:
        user_rating.append([rating.user_id, rating.song_id, rating.ratings])

    print(user_rating)

    for i in range(len(user_data)):
        ratings.loc[i + 1] = [1, 5, 3]  # Test data

    ratings = ratings.fillna(0)  # Replaces NaN with 0
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

    return jsonify({'similar to': most_similar_to(int(user_id))}), 200
