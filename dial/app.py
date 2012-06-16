import os

from flask import Flask, make_response, request

import plivo

app = Flask(__name__)

@app.route('/dial/', methods=['GET'])
def dial():
    """
    GET parameter:
        numbers - a comma seperated values of numbers
                which will be dialed
    """
    try:
        numbers = request.args['numbers']
        numbers = numbers.split(',')
    except KeyError:
        numbers = get_numbers()

    try:
        From = request.args['From']
    except KeyError:
        From = None

    if not numbers:
        response = make_response("Please provide numbers")
        return response

    r = plivo.Response()
    r.addSpeak('Welcome, We are connecting your call')
    if From:
        d = r.addDial(callerId = From)
    else:
        d = r.addDial()

    for number in numbers:
        d.addNumber(number)

    response = make_response(r.to_xml())
    response.headers['Content-Type'] = 'text/xml'
    return response


def get_numbers():
    """
    Used when there is no number provided in the GET parameter
    of /dial
    """
    return None

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
