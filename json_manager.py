import json
from collections import Counter
from json import JSONDecodeError
from os import path


class JSONManager:

    def __init__(self, filename):
        self._filename = filename
        self._verify_file_exists()

    def _verify_file_exists(self):
        if not path.exists(self._filename):
            f = open(self._filename, 'w+')
            f.close()

    def update_counter(self, counter):
        data = None
        try:
            with open(self._filename, "r") as read_file:
                try:
                    data = json.load(read_file)
                except JSONDecodeError:
                    pass
                    # file is empty or corrupted

            aggregated_counter = Counter(data)
            aggregated_counter.update(counter)
        except (ValueError, IOError) as err:
            raise RuntimeError(f"Error Updating results to Stats File: {str(err)}")

        with open(self._filename, "w+") as write_file:
            json.dump(aggregated_counter, write_file)

    def get_counters(self, word):
        try:
            with open(self._filename, "r") as read_file:
                data = json.load(read_file)

            result = 0 if word not in data else data[word]
            return result

        except JSONDecodeError:
            raise RuntimeError("Stats File empty")

        except (ValueError, IOError):
            raise RuntimeError("Error Reading Stats File")
