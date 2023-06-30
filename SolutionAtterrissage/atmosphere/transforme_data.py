def flatten_json(data, prefix=''):
    """
    Cette fonction permet de transformer la base de données obtenue par Windy en base
    de données plus facilement exploitable

    Args:
        data (json): la base de données à transformer

    Returns:
        flattened: la base de données transformée
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