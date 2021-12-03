from math import sqrt
from random import randint
import matplotlib.pyplot as plt

class Node(object):

    count = 0

    def __init__(self, points=[], length=0):
        self.setAxis(length, points)
        points, median = self.findMedian(points)
        self.setRoot(points, median)
        self.setLeft(points, median, length)
        self.setRight(points, median, length)

    def setAxis(self, length=0, points=[]):
        self.axis = 0
        if points:
            self.axis = length % len(points[0])

    def getAxis(self):
        return self.axis

    def setRoot(self, points=[], median=0):
        self.root = None
        if points:
            self.root = points[median]

    def getRoot(self):
        return self.root

    def setLeft(self, points=[], median=0, length=0):
        self.left = None
        if points:
            self.left = Node(points[:median], length+1)

    def getLeft(self):
        return self.left

    def setRight(self, points=[], median=0, length=0):
        self.right = None
        if points:
            self.right = Node(points[median+1:], length+1)

    def getRight(self):
        return self.right

    def findMedian(self, points=[]):
        axis = self.getAxis()
        median = 0
        if points:
            points = sorted(points, key=lambda point: point[self.axis])
            median = int(len(points)/2)
        return points, median

    def calculate_manhattan_distance(self, x, y):
        return ((abs(x[0]-y[0]))**2)+((abs(x[1]-y[1]))**2)

    def calculate_euclidean_distance(self, x, y):
        return sqrt(((x[0]-y[0])**2)+((x[1]-y[1])**2))

    def calculate_chebychev_distance(self, x, y):
        return max(abs(x[0]-y[0]), abs(x[1]-y[1]))

    def point_selection(self, query_point, is_near=True, is_axis=False):
        selected_point = self.right
        if self.root[self.axis] > query_point[self.axis]:
            selected_point = self.left
        if not is_near:
            if selected_point is self.left:
                return self.right
            else:
                return self.left
        elif is_axis:
            axis_point = list(query_point)
            axis_point[self.axis] = self.root[self.axis]
            return axis_point
        return selected_point

    def nearest_neighbour(self, query_point, neighbour=None):
        Node.count+=1
        if not self.root:
            return neighbour

        if not neighbour:
            neighbour = self.root

        if  self.calculate_manhattan_distance(neighbour, query_point) > self.calculate_manhattan_distance(self.root, query_point):
            neighbour = self.root

        selected_point = self.point_selection(query_point)
        neighbour = selected_point.nearest_neighbour(query_point, neighbour)
        
        axis_point = self.point_selection(query_point, is_axis=True)
        if self.calculate_manhattan_distance(axis_point, query_point) < self.calculate_manhattan_distance(neighbour, query_point):
            neighbour = self.point_selection(query_point, False).nearest_neighbour(query_point, neighbour)

        return neighbour


if __name__ == '__main__':
    n = None
    while True:
        try:
            n = int(input("Please enter total number of points: "))
            if type(n) == int:
                break
        except Exception:
            print("===== Please enter valid number =====")

    points = []
    for i in range(n):
        point = (randint(0, n), randint(0, n))
        points.append(point)

    tree = Node(points)
    query_point = (randint(0, n), randint(0, n))
    print("The query point co-ordinate :", query_point)
    neighbour = tree.nearest_neighbour(query_point)
    print("The nearest neighbour point co-ordinate :", neighbour)
    print("Total number of points: ", n)
    print("Total number of search iterations: ", Node.count)
    points.remove(neighbour)
    plt.scatter(*zip(*points), color="green")
    plt.scatter(query_point[0], query_point[1], color="red")
    plt.scatter(neighbour[0], neighbour[1], color="blue")
    plt.show()