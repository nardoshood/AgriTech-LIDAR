import json

def read_json(filename):
    """
    a script that reads
    json file and return
    a dictionary
    """
    with open(filename, 'r') as openfile:
        result = json.load(openfile)
    return result

def read_csv(filename):
    pass

