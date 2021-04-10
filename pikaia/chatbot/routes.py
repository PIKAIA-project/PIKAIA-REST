from datetime import timedelta, datetime, date

from sqlalchemy import func

from pikaia import app, db
from pikaia.token import token_required
from pikaia.models.models import Chat, User
from flask import request, jsonify, session
from pikaia.emotion_analysis import preProcessEmotionModel
import uuid
import requests
import numpy as np

# class Name on Emotions
class_names = ['joy', 'fear', 'anger', 'sadness', 'neutral']


# TODO: add validation and error handling code
# json request body structure
# { 'userInput' : 'hi, How's the weather today?' }
@app.route('/chat', methods=['POST'])
@token_required
def create_chat_conversation(current_user):
    # admin users cannot have chats
    if current_user.admin:
        return jsonify({'message': 'Admin users cannot create chat conversations!'})

    client_data = request.get_json(force=True)
    # Encoding json
    encodedRequest = ([client_data['userInput']])

    user_emotion = (class_names[np.argmax(preProcessEmotionModel(encodedRequest))])

    brain_shop_payload = {
        'bid': '155151',
        'key': 'tKJeOa4WLS84Eyee',
        'uid': current_user.id,
        'msg': client_data['userInput']
    }
    brain_shop_endpoint = 'http://api.brainshop.ai/get?'

    try:
        # GET request to brain API
        chatbot_request = requests.get(brain_shop_endpoint, params=brain_shop_payload)
        brain_data = chatbot_request.json()
        chatbot_sentence = brain_data['cnt']

    except:
        return jsonify({'error': 'Brainshop service unavailable'}), 503

    # Saving data
    new_conversation = Chat(public_id=str(uuid.uuid4()), user_sentence=client_data['userInput'],
                            chatbot_sentence=chatbot_sentence, user_id=current_user.id, user_emotion=user_emotion)
    db.session.add(new_conversation)
    db.session.commit()

    return jsonify(
        {'chatBotResponse': chatbot_sentence,
         'userInputEmotion': user_emotion
         })


@app.route('/chat', methods=['GET'])
@token_required
def get_all_chat_conversations(current_user):
    # admin users cannot have chats
    if current_user.admin:
        return jsonify({'message': 'Admin users cannot read user chat conversations!'})

    conversations = Chat.query.filter_by(user_id=current_user.id).all()

    # an array to hold all the dictionaries
    output = []
    # inserting each to-do into it's own dictionary
    for conversation in conversations:
        conversation_data = {'public_id': conversation.public_id, 'user_sentence': conversation.user_sentence,
                             'chatbot_sentence': conversation.chatbot_sentence,
                             'user_emotion': conversation.user_emotion, 'date_time': conversation.date_time}
        output.append(conversation_data)

    return jsonify({'conversations': output}), 200


@app.route('/chat/<user_public_id>', methods=['DELETE'])
@token_required
def admin_delete_user_chat_conversations(current_user, user_public_id):
    # normal users cannot delete other user's chats
    if not current_user.admin:
        return jsonify({'message': 'This delete route is not for Admin users user route /chat/[user_id]'})

    user = User.query.filter_by(public_id=user_public_id).first()
    if not user:
        return jsonify({'message': 'no such user'})

    userId = user.id

    deleted = 0
    while True:
        conversation = Chat.query.filter_by(user_id=userId).first()
        # no conversation in iteration
        if not conversation:
            break

        db.session.delete(conversation)
        deleted += 1

    if deleted == 0:
        return jsonify({'message': 'No conversations of user {} deleted!'.format(user_public_id)})

    db.session.commit()
    return jsonify({'message': 'chat data of user {} successfully deleted'.format(user_public_id)})


@app.route('/chat', methods=['DELETE'])
@token_required
def user_delete_all_chat_conversations(current_user):
    # admin users cannot use this route
    if current_user.admin:
        return jsonify({'message': 'This delete route is not for Admin users user route /chat/[user_id]'})

    deleted = 0
    while True:
        conversation = Chat.query.filter_by(user_id=current_user.id).first()
        # no conversation in iteration
        if not conversation:
            break

        db.session.delete(conversation)
        deleted += 1

    if deleted == 0:
        return jsonify({'message': 'No conversations to delete!'})

    db.session.commit()
    return jsonify({'message': 'all conversations successfully deleted'})


@app.route('/chart_days/<days>', methods=['GET'])
@token_required
def get_all_chart_days(current_user, days):
    current_time = datetime.now().utcnow()

    if current_user.admin:
        return jsonify({'message': 'Admin users cannot read user chat conversations!'})

    last_week = current_time - timedelta(days=int(days))

    chart_days = Chat.query.filter(
        Chat.date_time > last_week).all()

    # an array to hold all the dictionaries
    output = []

    for chartData in chart_days:
        conversation_data = {'public_id': chartData.public_id, 'user_sentence': chartData.user_sentence,
                             'chatbot_sentence': chartData.chatbot_sentence,
                             'user_emotion': chartData.user_emotion, 'date_time': chartData.date_time}
        output.append(conversation_data)

    return jsonify({'chart_daily': output})


@app.route('/chart_hours/<hours>', methods=['GET'])
@token_required
def get_all_chart_hours(current_user, hours):
    current_hour = datetime.now().utcnow()

    if current_user.admin:
        return jsonify({'message': 'Admin users cannot read user chat conversations!'})

    last_week = current_hour - timedelta(hours=int(hours))
    chart_hours = Chat.query.filter(
        Chat.date_time > last_week).all()

    # an array to hold all the dictionaries
    output = []
    # inserting each to-do into it's own dictionary

    for chartData in chart_hours:
        conversation_data = {'public_id': chartData.public_id, 'user_sentence': chartData.user_sentence,
                             'chatbot_sentence': chartData.chatbot_sentence,
                             'user_emotion': chartData.user_emotion, 'date_time': chartData.date_time}
        output.append(conversation_data)

    return jsonify({'chart_daily': output})

    # start = date(year=2021, month=4, day=1)
    # end = date(year=2021, month=4, day=10)
    # chart_week = Chat.query.filter(Chat.date_time <= end).filter(Chat.date_time >= start)
    # chart_week = Chat.query.filter(Chat.date_time <= current_time - timedelta(days=1))
