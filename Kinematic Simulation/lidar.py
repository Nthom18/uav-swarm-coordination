'''
Using the principle of Ray Marching 
from Sebastion Lague Youtube video:

https://www.youtube.com/watch?v=Cp5WWtMoeKg&ab_channel=SebastianLague
'''

import math
import numpy as np
from vector import Vector2D

import constants

THRESHOLD = 0.1
MAX_MARCHING_STEPS = 15
FULL_CIRCLE = 360
RESOLUTION = 1 / 8

class LiDAR():

    def __init__(self, originPoint, obstacleList, canvas):
        self.oPos = originPoint.position
        self.oDir = originPoint.velocity.norm()
        self.range = originPoint.perception
        self.obstacles = obstacleList
        self.sensorReadings = []

        # DEBUG visualization
        self.canvas = canvas
        self.distanceCircle = self.canvas.create_oval(0, 0, 0, 0, fill = constants.COLOUR_GREY, outline = "", tags = "grey")


    def update(self, originPoint):
        # DEBUG visualization
        self.canvas.delete("red")
        self.canvas.delete("grey")
        # -------------------

        self.oPos = originPoint.position
        self.oDir = originPoint.velocity.norm()

        self.sensorReadings.clear()
        self.rayMarching()
        

    def rayMarching(self):
        for i in range(int(FULL_CIRCLE * RESOLUTION)):
            dot = self.sphereTracing(self.oDir.rotate(math.radians(i / RESOLUTION)))
            self.sensorReadings.append(self.oPos.distance_to(dot))

            # DEBUG
            # self.makeDot(dot, 2)

        # DEBUGGING ------------------ Show fov dots
        if len(self.sensorReadings) != 0:
            step_angle = 360 / len(self.sensorReadings)

        fov = math.ceil(len(self.sensorReadings) * 1/16)
        left = self.sensorReadings[-fov:]
        right = self.sensorReadings[:fov]

        for i, d in enumerate(left + right):
            dir = self.oPos + self.oDir.rotate(math.radians((i - fov) * step_angle)) * d
            self.makeDotBlue(dir, 2)
        # -----------------------------

    def sphereTracing(self, dir):
        p = self.oPos
        distToScene = self.signedDistToScene(p)

        for i in range(MAX_MARCHING_STEPS):
            p = p + dir * distToScene
            distToScene = self.signedDistToScene(p)

            if distToScene < THRESHOLD:
                return p
            
            if self.oPos.distance_to(p) > self.range:
                return self.oPos + dir * self.range

        return self.oPos + dir * self.range
        

    def signedDistToScene(self, p):
        distToScene = constants.BOARD_SIZE

        for circle in self.obstacles:
            distToCircle = self.signedDistToCircle(p, circle)
            distToScene = min(distToCircle, distToScene)

        # # DEBUG
        # self.drawDistance(distToScene)
        # print(distToScene)
        return distToScene


    def signedDistToCircle(self, p, circle):
        centre = Vector2D(circle[0], circle[1])
        radius = circle[2]
        return self.length(centre - p) - radius


    def length(self, v):
        return np.sqrt(v.x**2 + v.y**2)


    # ********V******** DEBUG FUNCTIONS ********V******** #


    def drawDistance(self, distance):
        x0 = self.oPos.x - distance
        y0 = self.oPos.y - distance
        x1 = self.oPos.x + distance
        y1 = self.oPos.y + distance

        self.canvas.coords(self.distanceCircle, x0, y0, x1, y1)

    
    def makeDot(self, p, r):
        x0 = p.x - r
        y0 = p.y - r
        x1 = p.x + r
        y1 = p.y + r
        return self.canvas.create_oval(x0, y0, x1, y1, fill = constants.COLOUR_RED, outline = "", tags = "red")

    def makeDotBlue(self, p, r):
        x0 = p.x - r
        y0 = p.y - r
        x1 = p.x + r
        y1 = p.y + r
        return self.canvas.create_oval(x0, y0, x1, y1, fill = constants.COLOUR_RED, outline = "", tags = "red")
