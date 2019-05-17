
import seaborn as sns
import matplotlib.pyplot as plt

from reader import Reader

class Visualizer:

    def __init__(self, reader):

        if not isinstance(reader, Reader):
            raise ValueError("'reader' is not an instrance of 'Reader'")

        sns.set(style='whitegrid')

        self.data = reader.data


    def countplot(self, header, title, squeeze=False, predicate=None, palette='Set3'):

        if not isinstance(header, str):
            raise ValueError("'header' is not an instrance of 'str'")

        if not isinstance(title, str):
            raise ValueError("'title' is not an instrance of 'str'")

        if header == 'DAY_OF_WEEK':
            order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        else:
            order = sorted(self.data[header].unique())

        data = self.data

        if predicate:
            data = data[predicate(data)]

        axes = sns.countplot(x=header, data=data, order=order, palette=palette)

        if header == 'MONTH':
            axes.set_xticklabels(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

        axes.set_title(title)

        axes.set(xlabel='', ylabel='')

        if squeeze:
            axes.set_xticklabels(axes.get_xticklabels(), rotation=90, fontsize=7, ha='left')

            plt.tight_layout()

        plt.show()


    def scatterplot(self, hue, title=None, palette='Set2'):

        axes = sns.scatterplot(x='Long', y='Lat', data=self.data, hue=hue, palette=palette, legend=False)

        axes.set(xlabel='Longitude', ylabel='Latitude')

        if title:
            axes.set_title(title)

        plt.show()


if __name__ == "__main__":

    reader = Reader('../data/crime.csv')

    visualizer = Visualizer(reader)

    visualizer.countplot('YEAR', 'Crimes per Year')

