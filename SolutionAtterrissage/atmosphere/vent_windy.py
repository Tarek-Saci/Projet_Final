def get_windy_data(lat, lon):
    """
    Cette fonction permet d'obtenir en temps réel les données météorologiques en un point donné

    Args:
        lat (float): La latitude du point recherché compris entre -89.99° et 90°
        lon (float): La longitude du point recherché appartenant aux nombres réels

    Returns:
        data: base de données contenant les données sous forme json
    """
    url_base = "https://node.windy.com/forecast/meteogram/ecmwf/"
    url_request = url_base + str(lat) + "/" + str(lon)
    import urllib.request, json
    with urllib.request.urlopen(url_request) as url:
        data = json.load(url)
        # data = pd.read_json(url)
    return data