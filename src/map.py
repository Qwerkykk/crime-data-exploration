import folium
from folium import IFrame
from folium import Popup
from folium.plugins import MarkerCluster
from IPython.core.display import display

from reader import Reader

table = """
<!DOCTYPE html>
<html>

<head>
    <style>
        #info {{
            font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }}

        #info td,
        #info th {{
            border: 1px solid #ddd;
            padding: 8px;
        }}

        #info tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}

        #info tr:hover {{
            background-color: #ddd;
        }}

        #info th {{
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: rgb(86, 76, 175);
            color: white;
        }}
    </style>
</head>

<body>

    <table id="info">
        <tr>
            <th>Incident Number</th>
            <th>{}</th>
        </tr>
        <tr>
            <td>{}</td>
            <td>{}</td>
        </tr>
    </table>

</body>

</html>
""".format

class Map:

    def __init__(self, reader, sample_size=500):

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


    def display(self, header,coloring_attr = 'YEAR', predicate=None, zoom_start=11, popup_width=400, popup_height=100):

        if not isinstance(header, str):
            raise ValueError("'header' is not an instance of 'str'")
        
        if not isinstance(coloring_attr,str):
            raise ValueError("'coloring_attr' is not an instance of 'str'")

        data = self.data[['INCIDENT_NUMBER', 'Lat', 'Long', header,coloring_attr]]

        if predicate:
            data = data[predicate(self.data)]

        locations, popups ,icons = {}, {}, {}

        available_colors = [ 'blue', 'green', 'purple', 'orange', 'darkred',
            'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue',
            'darkpurple', 'gray']
        
        unique_tag = list(set(data[coloring_attr]))
    
        color_pallete = {}
        
        for tag in unique_tag:
            color_pallete[tag] = available_colors[unique_tag.index(tag)]
        
        for key in color_pallete.keys():
            print('<' + str(key) +': ' + str(color_pallete[key]) + '>',end =" ")
        
        formatted_header = header.replace('_', ' ').title()

        for _, row in data.iterrows():

            if not row[header] in locations:
                locations[row[header]] = []
                popups[row[header]] = []
                icons[row[header]] = []

            locations[row[header]].append([row['Lat'], row['Long']])    
            
            icons[row[header]].append(folium.Icon(color=color_pallete[row[coloring_attr]]))
            
            html = table(formatted_header, row['INCIDENT_NUMBER'], str(row[header]).title())

            ifrm = IFrame(html=html, width=popup_width, height=popup_height)
            popups[row[header]].append(Popup(ifrm))

        underlying = folium.Map(location=[self.center_x, self.center_y], zoom_start=zoom_start)

        for key in locations.keys():

            group = folium.FeatureGroup(str(key).title())
        
            group.add_child(MarkerCluster(locations[key], popups[key],icons[key]))

            underlying.add_child(group)

        underlying.add_child(folium.LayerControl())

        display(underlying)


if __name__ == '__main__':

    m = Map(Reader('../data/crime.csv'))

    m.display('OFFENSE_CODE_GROUP')

