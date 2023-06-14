# recursive function to flatten nested fields
def flatten_json(data, prefix=''):
    """Cette fonction permet d'applatir la base de données

    Keyword arguments:
    data -- base de données au format json non applatie

    Renvoie une base de données applatie
    """
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