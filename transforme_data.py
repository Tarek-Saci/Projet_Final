# recursive function to flatten nested fields
def flatten_json(data, prefix=''):
    if isinstance(data, dict):
        flattened = {}
        for key, value in data.items():
            flattened.update(flatten_json(value, prefix + key + '_'))
        return flattened
    elif isinstance(data, list):
        flattened = {}
        for i, item in enumerate(data):
            flattened.update(flatten_json(item, prefix + str(i) + '_'))
        return flattened
    else:
        return {prefix[:-1]: data}