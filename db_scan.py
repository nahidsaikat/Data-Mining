import math
import csv
from decimal import Decimal


class Point:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class DBScanner:
    def __init__(self, eps, min_pts):
        self.noise = -1
        self.eps = eps
        self.min_pts = min_pts
        self.data = self.read_data()
        self.label = [0] * len(self.data)

    def read_data(self):
        data = []
        with open("Iris.csv", "rb") as file_obj:
            reader = csv.reader(file_obj)
            counter = 0
            for row in reader:
                temp_dict = {
                    'id': counter,
                    'x': Decimal(row[1]),
                    'y': Decimal(row[2])
                }
                data.append(Point(**temp_dict))
                counter += 1

        return data

    def db_scan(self):
        C = 0

        for point in self.data:
            if self.label[point.id]:
                continue
            
            neighbors = self.range_query(point)
            if len(neighbors) < self.min_pts:
                self.label[point.id] = self.noise
                continue
            
            C += 1
            self.label[point.id] = C
            for nei in neighbors:
                if self.label[nei.id] == self.noise:
                    self.label[nei.id] = C
                if self.label[nei.id]:
                    continue
                
                self.label[nei.id] = C
                nei_neighbors = self.range_query(nei)
                if len(nei_neighbors) >= self.min_pts:
                    neighbors.extend(nei_neighbors)

    def range_query(self, P):
        neighbors = []
        for Q in self.data:
            if (self.dist(P, Q) <= self.eps):
                neighbors.append(Q)
        return neighbors

    def dist(self, p, q):
        x = (p.x - q.x)
        y = (p.y - q.y)
        return math.sqrt(x*x + y*y)

    def print_clusters(self):
        label = set(self.label)
        for item in label:
            print 'Cluster # ', item


if __name__ == '__main__':
    scanner = DBScanner(0.1, 5)
    scanner.db_scan()
    scanner.print_clusters()

