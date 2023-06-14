
def get_windy_data(lat, lon):
    """Cette fonction permet d'obtenir en temps réel les données
    météorologiques en un point donné à partir du site Windy.com.

    Keyword arguments:
    lat -- latitude du point recherché : flottant compris entre -89.99° et 90°
    lon -- longitude du point recherché : flottant quelconque

    Renvoie une base de données météorologiques
    """
    url_base = "https://node.windy.com/forecast/meteogram/ecmwf/"
    url_request = url_base + str(lat) + "/" + str(lon)
    import urllib.request, json
    with urllib.request.urlopen(url_request) as url:
        data = json.load(url)
        # data = pd.read_json(url)
    return data