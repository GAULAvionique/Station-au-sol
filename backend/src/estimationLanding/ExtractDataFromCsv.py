import csv
from pathlib import Path

from backend.src.estimationLanding.EstimateLanding import EstimateLanding
from backend.src.estimationLanding.dataObject.DataStructureExcel import DataStructureExcel
from backend.src.estimationLanding.dataObject.FlightData import FlightData


def readFile(path):
    print(path)

    base_path = Path(__file__).parent
    file_path = (base_path / path).resolve()

    altitudes = []
    latitudes = []
    longitudes = []
    times = []
    countFirst = True

    with open(file_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if countFirst:
                countFirst = False
                continue
            times.append(float(row[DataStructureExcel['TIME'].value]))
            altitudes.append(float(row[DataStructureExcel['ALTITUDE'].value]))
            longitudes.append(float(row[DataStructureExcel['LONGITUDE'].value]))
            latitudes.append(float(row[DataStructureExcel['LATITUDE'].value]))
        flightData = FlightData(times, altitudes, longitudes, latitudes)
    return flightData

flightData = readFile("../../../DATA/2024-08-19_005016_formatted.csv")

estimateLanding = EstimateLanding(flightData)

estimateLanding.estimateLandingPosition()