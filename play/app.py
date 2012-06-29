import os

from flask import Flask, make_response, request

import plivo
import redis

app = Flask(__name__)
app.debug = True

redis_url = os.getenv('REDISTOGO_URL', 'redis://192.168.2.31:6379')
redis = redis.from_url(redis_url)

trumpet_sound = 'https://s3.amazonaws.com/plivocloud/Trumpet.mp3'

auth_id = 'MANWVLYTK4ZWU1YTY4ZT'
auth_token = 'YzAyMWI3MjI2OTJmZmE1YTg2ZmFlNzA2YTZjNGE4'
p = plivo.RestAPI(auth_id, auth_token)

@app.route('/play/', methods=['GET'])
def dial():
    try:
        From = request.args['From']
        CallUUID = request.args['CallUUID']
        redis.set(From, CallUUID)
    except KeyError:
        From = None
        CallUUID = None

    r = plivo.Response()
    speak_parameters = {
            'language':'en-US',
            'loop':'1',
            'voice':'WOMAN',
            }

    r.addSpeak('Welcome to Plivo demo test.', **speak_parameters)
    play_parameters = {
            'loop':'50',
            }
    r.addPlay('http://s3.amazonaws.com/plivocloud/music.mp3', **play_parameters)

    response = make_response(r.to_xml())
    response.headers['Content-Type'] = 'text/xml'
    return response

@app.route('/hangup/', methods=['GET'])
def hangup():
    try:
        From = request.args['From']
        CallUUID = request.args['CallUUID']

        if CallUUID == redis.get(From):
            redis.delete(From)

    except KeyError:
        pass
    
    return "Done"



@app.route('/play_music/', methods=['GET'])
def music():
    """
    parameters:
        GET - number, use the phone number you want to play music to.
    """
    try:
        phone_number = request.args['number']
    except KeyError:
        return 'Please Provide a Number'

    call_uuid = redis.get(phone_number)
    play_parameters = {
            'call_uuid':call_uuid,
            'urls':trumpet_sound,
            'loop':True,
            }
    response = p.play(play_parameters)
    return 'Done'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
