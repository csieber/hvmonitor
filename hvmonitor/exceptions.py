
class NoHVInstanceFound(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return "No HV instance found!"
