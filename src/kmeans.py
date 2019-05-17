
from re import sub

from sklearn import cluster

from reader import Reader
from visualizer import Visualizer

class KMeans:

    def __init__(self, reader):

        if not isinstance(reader, Reader):
            raise ValueError("'reader' is not an instance of 'Reader'")

        self.data = reader.data


    def fit(self, n_clusters, header=None):

        if not isinstance(n_clusters, int) or n_clusters <= 0:
            raise ValueError("'n_clusters' must have an integer value greater than zero")

        if header:

            if not isinstance(header, str):
                raise ValueError("'header' is not an instance of 'str'")

            print('<LOG>: Clustering according to geographical location and', "'" + header.replace('_', ' ').title() + "'")

            header = header + '_FACTORIZED'

            data = self.data[['Long', 'Lat', header]]

        else:

            print('<LOG>: Clustering according to geographical location')

            data = self.data[['Long', 'Lat']]

        print('<LOG>: Running kmeans with', '{0:2}'.format(n_clusters), 'clusters')

        return cluster.KMeans(n_clusters=n_clusters).fit(data).labels_.astype(float)


if __name__ == '__main__':

    reader = Reader('../data/crime.csv')

    Visualizer(reader).scatterplot(KMeans(reader).fit(2))

