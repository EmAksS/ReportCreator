import json

def load_data(request_data):
    try:
        return json.loads(json.dumps(request_data["data"]))
    except TypeError:
        # list indices must be integers or slices, not str
        return json.loads(json.dumps(request_data))
    