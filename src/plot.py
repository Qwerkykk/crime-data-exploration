
import re

import seaborn as sb
import matplotlib.pyplot as plt

from reader import Reader

class Plotter:

    def __init__(self, reader):

        if not isinstance(reader, Reader):
            raise ValueError("'reader' is not an instrance of 'Reader'")

        sb.set(style='whitegrid')

        self.data = reader.data


    def countplot(self, header, palette='Set3'):

        if not isinstance(header, str):
            raise ValueError("'header' is not an instrance of 'str'")

        if header == 'DAY_OF_WEEK':
            order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        else:
            order = sorted(self.data[header].unique())

        axes = sb.countplot(x=header, data=self.data, order=order, palette=palette)

        axes.set(xlabel=header.replace('_', ' ').title(), ylabel='')

        plt.show()


if __name__ == "__main__":

    reader = Reader('../data/crime.csv')

    # Question 1
    plotter = Plotter(reader)

    plotter.countplot('YEAR')

    plotter.countplot('MONTH')

    plotter.countplot('DAY_OF_WEEK')

    plotter.countplot('DISTRICT')

    # Questeion 3
    plotter.countplot('HOUR')

    plotter.countplot('TIME')

    # ax = sb.countplot(x='HOUR', data=reader.data)

    # plt.show()

    # ax = sb.countplot(x='YEAR', hue='SHOOTING', data=reader.data[reader.data['SHOOTING'] == 'Y'])

    # plt.show()

