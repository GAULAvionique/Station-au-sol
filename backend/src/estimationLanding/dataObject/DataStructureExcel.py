from enum import Enum
class DataStructureExcel(Enum):
    TIME = 0
    FLIGHT_MODE = 1
    STAT_IGNITER_1 = 2
    STAT_IGNITER_2 = 3
    STAT_IGNITER_3 = 4
    STAT_IGNITER_4 = 5
    STAT_ACCELEROMETER = 6
    STAT_BAROMETER = 7
    STAT_GPS = 8
    STAT_SD = 9
    TEMPERATURE = 10
    #Pouruqoi on a ces deux paramères,
    # on ne devrait pas convertir sur la station au sol en ft pour réduire la taille des paquets?
    ALTITUDE = 11
    ALTITUDE_FT = 12
    SPEED = 13
    ACCELERATION = 14
    GPS_FIX = 15
    LATITUDE = 16
    LONGITUDE = 17
    PITCH = 18
    YAW = 19
    ROLL = 20
    BATTERIE_1 = 21
    BATTERIE_2 = 22
    BATTERIE_3 = 23