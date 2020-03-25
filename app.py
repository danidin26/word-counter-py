from flask import Flask, make_response, request
import urllib
import os
from word_counter import processor_service as processor

app = Flask(__name__)

_INPUT_TYPES = ('text', 'url', 'local')


def _check_if_url_exists(url):
    try:
        urllib.request.urlopen(url)
    except (urllib.error.HTTPError, urllib.error.URLError):
        raise urllib.error.URLError
    return True


def _check_if_file_exists(file_path):
    try:
        os.path.isfile(file_path)
    except FileNotFoundError:
        raise FileNotFoundError


def _validate(input_type, data):
    if input_type == 'url':
        _check_if_url_exists(data)
    if input_type == 'local':
        _check_if_file_exists(data)
    # for data in request body always return True:


def _process_input(input_type, data):
    if input_type == 'url':
        processor.process_input_from_url(data)
        return
    if input_type == 'local':
        processor.process_input_file(data)
        return
    processor.process_input_from_request(data)


@app.route("/count/<string:input_type>", methods=["POST"])
def count(input_type):
    if input_type not in _INPUT_TYPES:
        return make_response(
            'Invalid input type "{input_type}", available input types: {}'.format(', '.join(_INPUT_TYPES)), '400')
    data = request.data
    if not data:
        return make_response('Request body must contain text / URL / local path to work on', '400')

    decoded = data.decode('utf-8')
    try:
        _validate(input_type, decoded)
        _process_input(input_type, data)
        return make_response("OK", '202')
    except RuntimeError as err:
        return make_response(err, 400)
    except FileNotFoundError:
        return make_response("input file does not exist", 400)
    except urllib.error.URLError:
        return make_response("error opening input url", 400)


@app.route("/statistics/<string:input_word>", methods=["GET"])
def stats(input_word):
    occurrences = processor.process_stats_for_word(input_word)
    return str(occurrences)


if __name__ == '__main__':
    app.run()
