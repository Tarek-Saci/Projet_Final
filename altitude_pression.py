import math
# L'argument doit être entré en mètres

def calcul_altitude_pression(altitude):
    #d'après l'ISA
    if altitude<11000:
        pression = 1013.25*(1-0.0065*altitude/288.15)**(9.81/(0.0065*287.04))
    else:
        pression = 226.32*math.exp(-9.81*(altitude-11000)/(287.04*216.65))
    return pression

#print(calcul_altitude_pression(8500))