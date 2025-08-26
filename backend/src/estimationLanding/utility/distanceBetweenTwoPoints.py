import math
import geopy

from geopy import distance
def distanceBetweenTwoPoints(point1:(float,float), point2:(float,float)):
    distanceKm = distance.distance(point1, point2).km
    #print(distanceKm)
    angle = getBearing(point1, point2)
    relativePoint = (distanceKm*math.cos(math.radians(angle)), distanceKm*math.sin(math.radians(angle)))
    return relativePoint

def getBearing(point1:(float, float), point2:(float, float)):
    lat1 = math.radians(point1[0])
    lon1 = math.radians(point1[1])

    lat2 = math.radians(point2[0])
    lon2 = math.radians(point2[1])

    dLon = lon2 - lon1
    y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
    x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
    brng = math.degrees(math.atan2(x, y))
    if brng < 0: brng+= 360
    return brng