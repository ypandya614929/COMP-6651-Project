import datetime
import rtree.index as Rtreelib
from math import sqrt
from random import randint
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class Node(object):

    # class variable
    count = 0

    # constructor
    def __init__(self, points=[], length=0):
        self.r_tree = None
        self.setAxis(length, points)
        points, median = self.findMedian(points)
        self.setRoot(points, median)
        self.setLeft(points, median, length)
        self.setRight(points, median, length)

    # getter & setter methods
    def setRtree(self, tree):
        self.r_tree = tree

    def getRtree(self):
        if self.r_tree:
            return self.r_tree
        return None

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

    # this method is used to find the median value from the
    # given set of points, it varies based on x, y axis as a key
    # when use along with KDTree construction
    def findMedian(self, points=[]):
        axis = self.getAxis()
        median = 0
        if points:
            points = sorted(points, key=lambda point: point[self.axis])
            median = int(len(points)/2)
        return points, median

    # distance calculation methods tried all three of them to
    # get the best time complexity.
    def calculate_manhattan_distance(self, x, y):
        return ((abs(x[0]-y[0]))**2)+((abs(x[1]-y[1]))**2)

    def calculate_euclidean_distance(self, x, y):
        return sqrt(((x[0]-y[0])**2)+((x[1]-y[1])**2))

    def calculate_chebychev_distance(self, x, y):
        return max(abs(x[0]-y[0]), abs(x[1]-y[1]))

    # select the next point from set of points while seraching for
    # neighbors respect to query point in KDTree
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

    # this method is used to calculate the nearest neighbour from
    # the set of points with respect to query point in KD Tree
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

    # This method is used to generate the RTree as mentioned RTree
    # library is already imported and mentioned in env requirement file
    def generateRTree(self, points):
        tree = Rtreelib.Rtree()
        for i, point in enumerate(points):
            tree.insert(i, point + point, point)
        self.setRtree(tree)

    # this method is used to calculate the nearest neighbour from
    # the set of points with respect to query point in RTree
    def nearest_neighbour_RTree(self, query_point):
        tree = self.getRtree()
        neighbour = (None, None)
        if tree:
            neighbours = list(tree.nearest(query_point, 1, objects='raw'))
            if neighbours:
                neighbour = neighbours[0]
        return neighbour


# python main method / start of program
if __name__ == '__main__':
    # taking a total number of points to run a query on
    n = None
    while True:
        try:
            n = int(input("Please enter total number of points: "))
            if type(n) == int:
                break
        except Exception:
            print("===== Please enter valid number =====")

    # set of points
    points = []
    for i in range(n):
        point = (randint(0, n), randint(0, n))
        points.append(point)

    # randomly find the query point within total number of points
    query_point = (randint(0, n), randint(0, n))
    print("Total number of points: ", n)
    print("The query point co-ordinate :", query_point)

    # KD Tree Generation and NN finding
    tree = Node(points)
    start_ts = datetime.datetime.now()
    neighbour = tree.nearest_neighbour(query_point) # only searching time is taken into consideration
    end_ts = datetime.datetime.now()
    print("The nearest neighbour point co-ordinate KDTree :", neighbour)
    # print("Total number of search iterations: ", Node.count)
    print("Total Search Time for KDTree : {0:.4f} ms".format((end_ts - start_ts).total_seconds()*1000))

    # R Tree Generation and NN finding
    rtree = Node()
    rtree.generateRTree(points)
    start_ts = datetime.datetime.now()
    neighbour = rtree.nearest_neighbour_RTree(query_point) #  only searching time is taken into consideration
    end_ts = datetime.datetime.now()
    print("The nearest neighbour point co-ordinate RTree :", neighbour)
    print("Total Search Time for RTree : {0:.4f} ms".format((end_ts - start_ts).total_seconds()*1000))

    # generating the graph for visualization if points are less than 1000
    # otherwise it won't show graph only calculations can be seen.
    if len(points) <= 1000:
        points.remove(neighbour)
        plt.scatter(*zip(*points), color="green")
        plt.scatter(query_point[0], query_point[1], color="red")
        plt.scatter(neighbour[0], neighbour[1], color="blue")
        red_label = mpatches.Patch(color='red', label='Query Point')
        blue_label = mpatches.Patch(color='blue', label='Neighbour Point')
        plt.legend(handles=[red_label, blue_label])
        plt.show()
