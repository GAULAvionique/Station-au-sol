from itertools import accumulate

import numpy as np
from matplotlib import pyplot as plt

from backend.src.estimationLanding.dataObject import FlightData
from backend.src.estimationLanding.utility.Ransac import RANSAC, LinearRegressor, square_error_loss, mean_square_error
from backend.src.estimationLanding.utility.distanceBetweenTwoPoints import distanceBetweenTwoPoints


class EstimateLanding:
    def __init__(self, flightData: FlightData):
        self.flightData = flightData
        self.cleanData()
        self.posInitial = (0, 0)
        self.nbDataPoint = 45

    def estimateLandingPosition(self):
        # TODO mettre une condition boolean pour voir les graphs ou juste avoir la data
        deltaAltitudes, driftsX, driftsY = self.estimateLinearFormulas()

        lastAltitudesValue = self.flightData.altitudes[len(self.flightData.altitudes)-1]
        driftsX = list(accumulate(driftsX))
        driftsY = list(accumulate(driftsY))

        timeUntilAltitude0 = lastAltitudesValue/(sum(deltaAltitudes)/len(deltaAltitudes))
        print("TIME TILL CRASH : ")
        print(timeUntilAltitude0)
        plt.figure(figsize=(8, 6))
        plt.plot(self.flightData.longitudes, self.flightData.latitudes, marker='o', linestyle='-', color='b', label='Flight Path')
        plt.title('Flight Path (Latitudes vs Longitudes)')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.grid(True)
        plt.legend()
        plt.show()

        plt.figure(figsize=(8, 6))
        plt.plot(self.flightData.times, self.flightData.altitudes, marker='o', linestyle='-', color='b', label=' Altitude rocket')
        plt.title('Altitude')
        plt.xlabel('Times')
        plt.ylabel('Altitudes')
        plt.grid(True)
        plt.legend()
        plt.show()

        plt.figure(figsize=(8, 6))
        plt.plot(self.flightData.times[-self.nbDataPoint:], deltaAltitudes, marker='o', linestyle='-', color='b', label=' Altitude rocket')
        plt.title('Altitude')
        plt.xlabel('Times')
        plt.ylabel('Altitudes')
        plt.grid(True)
        plt.legend()
        plt.show()

        deltaX, deltaY = self.estimateDrift(driftsX, driftsY, self.flightData.times[-self.nbDataPoint:])
        print(deltaX)
        print(deltaY)
        distanceFromLastDataPoint = (deltaX*timeUntilAltitude0, deltaY*timeUntilAltitude0)
        print("Distance from last point received")
        print("Distance X")
        print(distanceFromLastDataPoint[0])

        print("Distance Y")
        print(distanceFromLastDataPoint[1])

        plt.figure(figsize=(8, 6))
        plt.plot(driftsX, driftsY, marker='o', linestyle='-', color='b', label=' Altitude rocket')
        plt.title('Drift')
        plt.xlabel('X (km)')
        plt.ylabel('Y (km)')
        plt.grid(True)
        plt.legend()
        plt.show()

        return 0
    def estimateLinearFormulas(self):
        mList = []
        longDeltaList = []
        self.posInitial = (self.flightData.latitudes[0], self.flightData.longitudes[0])
        distanceX = []
        distanceY = []

        for id, altitude in enumerate(self.flightData.altitudes):
            if id != 0 and id != len(self.flightData.altitudes):
                deltaTime = self.flightData.times[id] - self.flightData.times[id-1]
                deltaAltitude = altitude - self.flightData.altitudes[id-1]
                deltaLong = self.flightData.longitudes[id] - self.flightData.longitudes[id-1]
                deltaLat = self.flightData.latitudes[id] - self.flightData.latitudes[id-1]

                pos1 = (self.flightData.latitudes[id], self.flightData.longitudes[id])
                pos2 = (self.flightData.latitudes[id-1], self.flightData.longitudes[id-1])

                distanceXY = distanceBetweenTwoPoints(pos1, pos2)
                distanceX.append(distanceXY[0])
                distanceY.append(distanceXY[1])
                m = deltaAltitude/deltaTime
                mList.append(m)
        #TODO comment identifier les deux pentes
        # de préférences ont n'aurait pas à se fier à la fusée

        return mList[-self.nbDataPoint:], distanceX[-self.nbDataPoint:], distanceY[-self.nbDataPoint:]
    def cleanData(self):
        altitudeMax = 0
        idMax = 0
        for idx, altitude in enumerate(self.flightData.altitudes):
            if altitude >= altitudeMax:
                altitudeMax = altitude
                idMax = idx

        self.flightData.times = self.flightData.times[idMax:]
        self.flightData.altitudes = self.flightData.altitudes[idMax:]
        self.flightData.latitudes = self.flightData.latitudes[idMax:]
        self.flightData.longitudes = self.flightData.longitudes[idMax:]

        for idx, altitude in sorted(enumerate(self.flightData.altitudes), reverse=True):
            if altitude == 0 or self.flightData.times[idx] == 0 or self.flightData.longitudes[idx]\
                == 0 or self.flightData.latitudes[idx] == 0:
                self.flightData.times.pop(idx)
                self.flightData.altitudes.pop(idx)
                self.flightData.latitudes.pop(idx)
                self.flightData.longitudes.pop(idx)

    def estimateDrift(self, driftsX, driftsY, times):
        #TODO clean up this mess
        regressor = RANSAC(model=LinearRegressor(), loss=square_error_loss, metric=mean_square_error)

        driftXArray = np.array(driftsX).reshape(-1, 1)
        driftYArray = np.array(driftsY).reshape(-1, 1)
        times = np.array(times).reshape(-1, 1)
        for idx, driftX in sorted(enumerate(driftXArray), reverse=True):
            if driftX == 0 and driftYArray[idx]:
                times.pop(idx)
                driftXArray.pop(idx)
                driftYArray.pop(idx)


        regressor.fit(times, driftXArray)

        plt.style.use("seaborn-darkgrid")
        fig, ax = plt.subplots(1, 1)
        ax.set_box_aspect(1)

        plt.scatter(times, driftsX)

        line = np.linspace(3000, 3500, num=100).reshape(-1, 1)
        predictionArray = regressor.predict(line)
        plt.plot(line, predictionArray, c="peru")
        plt.show()

        deltaTimes = 3500 - 3000
        deltaX = predictionArray[99] - predictionArray[0]
        deltaX = deltaX/deltaTimes

        regressor2 = RANSAC(model=LinearRegressor(), loss=square_error_loss, metric=mean_square_error)
        regressor2.fit(times, driftYArray)

        plt.style.use("seaborn-darkgrid")
        #fig, ax = plt.subplots(1, 1)
        ax.set_box_aspect(1)

        plt.scatter(times, driftsY)

        line = np.linspace(3000, 3500, num=100).reshape(-1, 1)
        predictionArray = regressor2.predict(line)
        plt.plot(line, predictionArray, c="peru")
        plt.show()

        deltaTimes = 3500 - 3000
        deltaY = predictionArray[99] - predictionArray[0]
        deltaY = deltaY / deltaTimes
        return deltaX, deltaY