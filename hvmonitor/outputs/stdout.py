import json


class PrintHandler(object):

    def __init__(self):
        pass

    def out(self, _, measurement):
        print(json.dumps(measurement, indent=4, sort_keys=True))
