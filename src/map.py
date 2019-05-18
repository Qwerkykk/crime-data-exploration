
import folium
from folium.plugins import MarkerCluster
from IPython.core.display import display

from reader import Reader

class Map:

    def __init__(self, reader, sample_size=500, zoom_start=11):

        self.zoom_start = zoom_start

        if not isinstance(reader, Reader):
            raise ValueError("'reader' is not an instance of 'Reader'")

        if sample_size:
            if not isinstance(sample_size, int) or sample_size <= 0:
                raise ValueError("'sample_size' must have an integer value greater than zero")

            self.sample_size = sample_size

            self.data = reader.data.sample(n=sample_size)

        else:
            self.data = reader.data

        self.center_x, self.center_y = self.data['Lat'].mean(), self.data['Long'].mean()


    def show(self, header, predicate=None):

        if not isinstance(header, str):
            raise ValueError("'header' is not an instance of 'str'")

        if predicate:
            data = self.data[predicate(self.data)][['Lat', 'Long', header]]

        else:
            data = self.data[['Lat', 'Long', header]]

        locations = {}

        for _, row in data.iterrows():

            if not row[header] in locations:
                locations[row[header]] = []

            locations[row[header]].append([row['Lat'], row['Long']])

        underlying = folium.Map(location=[self.center_x, self.center_y], zoom_start=self.zoom_start)

        for key in locations.keys():

            group = folium.FeatureGroup(str(key).title())

            group.add_child(MarkerCluster(locations[key], len(locations[key]) * [key]))

            underlying.add_child(group)

        underlying.add_child(folium.LayerControl())

        display(underlying)


if __name__ == '__main__':

    m = Map(Reader('../data/crime.csv'))

    m.show('OFFENSE_CODE_GROUP')

