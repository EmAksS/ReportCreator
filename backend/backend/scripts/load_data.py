import json

def load_data(request_data):
    print("request.data is ", request_data)

    try:
        return json.loads(json.dumps(request_data["data"]))
    except TypeError:
        # list indices must be integers or slices, not str
        print("oops, no [data] in request data")
        return json.loads(json.dumps(request_data))
    