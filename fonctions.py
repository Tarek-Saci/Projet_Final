def get_windy_data()

    url_request = url_base + str(latitude) + "/" + str(longitude)
    import urllib.request, json
    with urllib.request.urlopen(url_request) as url:
        data = json.load(url)