#Ce programme permet d'obtenir en temps réel les données météorologiques en un point donné
#Ce point doit être repéré par ses coordonnées GPS (latitude, longitude). La latitude doit être un flottant
# compris entre -89.99° et 90° tandis que la longitude peut être un flottant quelconque
def get_windy_data(lat, lon):
    url_base = "https://node.windy.com/forecast/meteogram/ecmwf/"
    url_request = url_base + str(lat) + "/" + str(lon)
    import urllib.request, json
    with urllib.request.urlopen(url_request) as url:
        data = json.load(url)
        # data = pd.read_json(url)
    return data