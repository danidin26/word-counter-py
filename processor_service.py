import re
from collections import Counter
from word_counter import json_manager
import requests as request

_PERSISTENT_DATA_FILE_PATH = "../statistics.json"

_READ_CHUNK_SIZE = 1 * 1024 * 1024
_REGEX_WORD_SEPARATOR = re.compile(r'\S+')
_REGEX_WORD_CLEANER = re.compile(r'[^A-Za-z]')

_json_manager = json_manager.JSONManager(_PERSISTENT_DATA_FILE_PATH)


def _tokenize(rawInput):
    res = []
    for match in _REGEX_WORD_SEPARATOR.finditer(rawInput):
        word_clean = _REGEX_WORD_CLEANER.sub('', match[0])
        if word_clean:
            res.append(word_clean)
    return res


def read_file_chunks(input_file):
    with open(input_file, 'r') as f:
        while True:
            buf = f.read(_READ_CHUNK_SIZE)
            if not buf:
                break

            # make sure we end on a space\nl\tab (word boundary)
            # this showed better time performance than the seek slice and concat logic used for url stream
            while not buf[-1].isspace():
                ch = f.read(1)
                if not ch:
                    break
                buf += ch
            yield buf
        yield ''  # handle the scene that the file is empty


def read_url_chunks(url):
    with request.get(url, stream=True) as response:
        if response.encoding is None:
            response.encoding = 'utf-8'
        concat = ''
        for chunk in response.iter_content(chunk_size=_READ_CHUNK_SIZE, decode_unicode=True):
            if concat:
                chunk = concat + chunk
                concat = ''

            if not chunk[-1].isspace():
                cut_index = chunk.rfind(" ")
                concat = chunk[cut_index:]
                chunk = chunk[:cut_index]

            yield chunk


def process_input_file(input_file):
    main_counter = Counter()
    for chunk in read_file_chunks(input_file):
        tokenized = _tokenize(chunk)
        main_counter.update(Counter(tokenized))

    _json_manager.update_counter(main_counter)


def process_input_from_url(url):
    main_counter = Counter()
    for chunk in read_url_chunks(url):
        tokenized = _tokenize(chunk)
        main_counter.update(Counter(tokenized))

    _json_manager.update_counter(main_counter)


def process_input_from_request(data):
    tokenized = _tokenize(data)
    counter = Counter(tokenized)
    _json_manager.update_counter(counter)


def process_stats_for_word(word):
    return _json_manager.get_counters(word)







