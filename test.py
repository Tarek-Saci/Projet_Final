def calcul_temperature(lat, lon, altitude):

    # Récupération des données dans la base de données de Windy
    meteo = get_windy_data(lat, lon)

    # Détermination de l'heure de la requête
    # En format POSIX
    posix_time = datetime.datetime.now().timestamp()
    #print(posix_time)
    # En format classique
    classical_time = datetime.datetime.fromtimestamp(posix_time)
    #print(classical_time)

    # Transformation du JSON en dataframe
    # flatten the JSON
    flattened = flatten_json(meteo)
    df = pd.DataFrame([flattened])

    # Détermination de l'heure répertoriée la plus proche de l'heure actuelle
    data_hours = df.filter(like="data_hours")

    i = 0
    #print(data_hours.iloc[0, i] / 1000)
    while posix_time > data_hours.iloc[0, i] / 1000:
        i += 1
    #print(i)
    if abs(posix_time - data_hours.iloc[0,i]) > abs(posix_time - data_hours.iloc[0, i-1]):
        i-=1

    # Liste des altitudes pour lesquelles les données sont recensées
    liste_altitude_pression = [150, 200, 250, 300, 400, 500, 600, 700, 800, 850, 900, 925, 950, 1000, 1013.25]

    # Calcul de l'altitude pression de l'avion
    altitude_pression_avion = calcul_altitude_pression(altitude)

    # Détermination de l'altitude recensée la plus proche de l'altitude de l'avion
    j = 0
    while altitude_pression_avion > liste_altitude_pression[j]:
        j += 1
    #print(j)
    if abs(altitude_pression_avion - liste_altitude_pression[j]) > abs(
            altitude_pression_avion - liste_altitude_pression[j - 1]):
        altitude_database = liste_altitude_pression[j - 1]
    else:
        altitude_database = liste_altitude_pression[j]
    # print(altitude_database)

    # Récupération des données recherchées dans la database
    if altitude_database != 1013.25:
        temperature = df[f'temp-{altitude_database}h_{i}']
    else:
        temperature = df[f'temp-surface_{i}']

    return temperature