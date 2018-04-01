import math
import csv
from decimal import Decimal


class Point:
    '''Point class.
    It has three attribute.
    x => Contains the x value of a point,
    y => Contains the y value of a point
    '''
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def __str__(self):
        return ', '.join([str(key) + ': ' + str(value) for key, value in self.__dict__.iteritems()])


class KMeans:
    '''The main class
    It takes eps and min_pts and calculates the clusters based on the data in Iris.csv.
    get_clusters method returns the final clusters.
    print_clusters method prints the final clusters.
    
    scanner = DBScanner(0.1, 5)
    scanner.db_scan()
    scanner.print_clusters()
    '''
    def __init__(self):
        self.data = self.read_data()
        self.means = [self.data[0], self.data[1], self.data[2]]
        self.clusters = [[] for _ in self.means]

    def read_data(self):
        '''Method that reads the data from CSV file.
        '''
        data = []
        with open("Iris.csv", "rb") as file_obj:            # Read CSV file
            reader = csv.reader(file_obj)
            counter = 0
            for row in reader:                              # Scan all row of CSV file
                temp_dict = {     
                    'x': Decimal(row[1]),
                    'y': Decimal(row[2])
                }
                data.append(Point(**temp_dict))             # Create Point object and add to data list
                counter += 1

        return data

    def k_means(self):
        '''Method that calculates the clusters.
        '''
        self.clusters = [[] for _ in self.means]

        for point in self.data:
            self.clusters[self.closest_cluster(point)].append(point)
        
        new_means = self.calculate_means()
        if not self.equals(new_means):
            self.means = new_means
            self.k_means()

    def closest_cluster(self, point):
        close_distance = Decimal('Infinity')
        cluster = 0
        for index, item in enumerate(self.means):
            if self.dist(point, item) < close_distance:
                close_distance = self.dist(point, item)
                cluster = index
        return cluster

    def dist(self, p, q):
        '''Method that calculates the distance.
        '''
        x = (p.x - q.x)
        y = (p.y - q.y)
        return math.sqrt(x*x + y*y)                         # Calculate distance between two point

    def calculate_means(self):
        means = []
        for cluster in self.clusters:
            avg_x = sum(point.x for point in cluster) / len(cluster)
            avg_y = sum(point.y for point in cluster) / len(cluster)
            means.append(Point(**{     
                'x': Decimal(avg_x),
                'y': Decimal(avg_y)
            }))
        return means

    def equals(self, new_means):
        flag = True
        for i in range(len(new_means)):
            if not self.subtract(self.means[i].x, new_means[i].x) < Decimal('0.001') or \
                not self.subtract(self.means[i].y, new_means[i].y) < Decimal('0.001'):
                flag = False
                break

        return flag

    def subtract(self, val1, val2):
        val1 = Decimal("{0:.2f}".format(val1))
        val2 = Decimal("{0:.2f}".format(val2))
        return abs(val1-val2)



if __name__ == '__main__':
    obj = KMeans()
    obj.k_means()
    print 'Means value are # \n'
    for item in obj.means:
        print item

