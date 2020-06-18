import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import subprocess
import random


class Circle:
    def __init__(self, points):
        if(len(points) == 0):
            self.ComputeFromNoPoints()
        elif(len(points) == 1):
            self.ComputeFromOnePoint(points[0])
        elif(len(points) == 2):
            self.ComputeFromTwoPoints(points)
        else:
            self.ComputeFromThreePoints(points)

    def IsPointInCircle(self, point):
        dist = np.linalg.norm(np.array(point)-self.center)
        return dist <= self.radius

    def IsValid(self, points):
        for point in points:
            if(not self.IsPointInCircle(point)):
                return False
        return True

    def ComputeFromNoPoints(self):
        self.radius = 0.0
        self.center = np.array([0, 0])

    def ComputeFromOnePoint(self, point):
        self.radius = 0.0
        self.center = point

    def ComputeFromTwoPoints(self, points):
        self.radius = np.linalg.norm(points[0]-points[1])/2
        self.center = (points[0]+points[1])/2

    def ComputeFromThreePoints(self, points):
        # checks if the circle may be contructed from two points
        possible_pairs = [[points[1], points[2]], [
            points[0], points[2]], [points[0], points[1]]]
        for i in range(3):
            circle = Circle(possible_pairs[i])
            if(circle.IsPointInCircle(points[i])):
                self.center = circle.center
                self.radius = circle.radius
                return
#       Equation of the cirlce is: x^2 + y^2 + 2*g*x + 2*f*y + r^2 = 0
#       where: (h = -g, k = -f) and radius r
        x1 = points[0][0]
        x2 = points[1][0]
        x3 = points[2][0]
        y1 = points[0][1]
        y2 = points[1][1]
        y3 = points[2][1]
        x12 = x1 - x2
        x13 = x1 - x3

        y12 = y1 - y2
        y13 = y1 - y3

        y31 = y3 - y1
        y21 = y2 - y1

        x31 = x3 - x1
        x21 = x2 - x1

        sx13 = x1**2 - x3**2

        sy13 = y1**2 - y3**2

        sx21 = x2**2 - x1**2
        sy21 = y2**2 - y1**2

        f = ((sx13) * (x12) + (sy13) * (x12) + (sx21) * (x13) +
             (sy21) * (x13)) / (2 * ((y31) * (x12) - (y21) * (x13)))
        g = ((sx13) * (y12) + (sy13) * (y12) + (sx21) * (y13) +
             (sy21) * (y13)) / (2 * ((x31) * (y12) - (x21) * (y13)))

        r2 = -(x1**2) - (y1**2) - 2 * g * x1 - 2 * f * y1

        center_x = -g
        center_y = -f

        self.radius = np.sqrt(center_x**2 + center_y**2 - r2)
        self.center = np.array([center_x, center_y])

    def PlotCircle(self, color='r'):
        circle = plt.Circle(self.center, self.radius, color=color, fill=False)
        plt.gcf().gca().add_artist(circle)
        plt.plot(self.center[0], self.center[1])

    def GetRadius(self):
        return self.radius

    def GetCenter(self):
        return self.center


def FindMinimumCircle(points, boundary):
    no_points_to_analyse = len(points) == 0
    if(no_points_to_analyse or len(boundary) == 3):
        return Circle(boundary)

    remaining_points = points[:-1]
    circle = FindMinimumCircle(remaining_points, boundary.copy())

    sample_point = points[-1]
    if(circle.IsPointInCircle(sample_point)):
        return circle

    boundary.append(sample_point)

    return FindMinimumCircle(remaining_points, boundary.copy())


def GenerateRandomPoints():
    n_points = random.randint(25, 60)
    coordinates = []
    for i in range(n_points):
        x_coordinates = -15+random.random()*30
        y_coordinates = -15+random.random()*30
        coordinates.append({"x": x_coordinates, "y": y_coordinates})

    Points = pd.DataFrame(coordinates)
    return Points


def PlotResults(circle, points):
    plt.scatter(points.x.values, points.y.values)
    circle.PlotCircle()

    center = circle.GetCenter()
    radius = circle.GetRadius()
    left_limit = center[0]-radius
    rigth_limit = center[0]+radius
    top_limit = center[1]+radius
    bottom_limit = center[1]-radius

    plt.xlim(left_limit, rigth_limit)
    plt.ylim(bottom_limit, top_limit)

    current_folder = os.getcwd()

    filename = os.path.join(current_folder, "enclosing_circle.png")
    print("Result is saved in", filename)
    plt.savefig(filename)

    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def main():

    points = GenerateRandomPoints()

    circle = FindMinimumCircle(points.values, [])

    PlotResults(circle, points)

    print("Minimum circle at: ", circle.center, " with radius=",
          circle.radius, " is enclosing ", len(points), " points")


if __name__ == '__main__':
    main()
