import math
import csv
from decimal import Decimal


class Point:
    '''Point class.
    It has three attribute.
    x => Contains the x value of a point,
    y => Contains the y value of a point,
    id => Unique number.
    '''
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class DBScanner:
    '''The main class
    It takes eps and min_pts and calculates the clusters based on the data in Iris.csv.
    get_clusters method returns the final clusters.
    print_clusters method prints the final clusters.
    
    scanner = DBScanner(0.1, 5)
    scanner.db_scan()
    scanner.print_clusters()
    '''
    def __init__(self, eps, min_pts):
        self.noise = -1                                     # Noise variable
        self.eps = eps                                      # Setting eps value
        self.min_pts = min_pts                              # Setting min_pts value
        self.data = self.read_data()                        # Main data set
        self.label = [0] * len(self.data)                   # Clusters as label

    def read_data(self):
        '''Method that reads the data from CSV file.
        '''
        data = []
        with open("Iris.csv", "rb") as file_obj:            # Read CSV file
            reader = csv.reader(file_obj)
            counter = 0
            for row in reader:                              # Scan all row of CSV file
                temp_dict = {                               # Temporary dictionary that contains x, y and id values
                    'id': counter,
                    'x': Decimal(row[1]),
                    'y': Decimal(row[2])
                }
                data.append(Point(**temp_dict))             # Create Point object and add to data list
                counter += 1

        return data

    def db_scan(self):
        '''Method that calculates the clusters.
        '''
        C = 0                                               # Cluster counter

        for point in self.data:
            if self.label[point.id]:                        # Previously processed in inner loop
                continue
            
            neighbors = self.range_query(point)             # Find neighbors
            if len(neighbors) < self.min_pts:               # Density check
                self.label[point.id] = self.noise           # Label as Noise
                continue
            
            C += 1                                          # next cluster label
            self.label[point.id] = C                        # Label initial point
            for nei in neighbors:                           # Process every neighbor point
                if self.label[nei.id] == self.noise:        # Change Noise to border point
                    self.label[nei.id] = C
                if self.label[nei.id]:                      # Previously processed
                    continue
                
                self.label[nei.id] = C                      # Label neighbor
                nei_neighbors = self.range_query(nei)       # Find neighbors
                if len(nei_neighbors) >= self.min_pts:      # Density check
                    neighbors.extend(nei_neighbors)         # Add new neighbors to seed set

    def range_query(self, P):
        '''Method that finds the neighbors.
        '''
        neighbors = []
        for Q in self.data:                                 # Scan all points in the data set
            if (self.dist(P, Q) <= self.eps):               # Compute distance and check epsilon
                neighbors.append(Q)                         # Add to result
        return neighbors

    def dist(self, p, q):
        '''Method that calculates the distance.
        '''
        x = (p.x - q.x)
        y = (p.y - q.y)
        return math.sqrt(x*x + y*y)                         # Calculate distance between two point

    def get_clusters(self):
        '''Method that returns list of clusters.
        '''
        return set(self.label)                              # Return all the clusters

    def print_clusters(self):
        '''Method that print the clusters.
        '''
        for item in self.get_clusters():                    # Scan all the clusters
            print 'Cluster # ', item                        # Print cluster


if __name__ == '__main__':
    scanner = DBScanner(0.1, 5)
    scanner.db_scan()
    scanner.print_clusters()

