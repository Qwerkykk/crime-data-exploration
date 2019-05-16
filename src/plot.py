
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

        axes = sb.countplot(x=header, data=data, order=order, palette=palette)

        if header == 'MONTH':
            axes.set_xticklabels(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

        axes.set_title(title)

        axes.set(xlabel='', ylabel='')

        if squeeze:
            axes.set_xticklabels(axes.get_xticklabels(), rotation=90, fontsize=7, ha='left')

            plt.tight_layout()

        plt.show()


if __name__ == "__main__":

    reader = Reader('../data/crime.csv')

    # Question No.1
    plotter = Plotter(reader)

    plotter.countplot('YEAR', 'Crimes per Year')

    plotter.countplot('MONTH', 'Crimes per Month')

    plotter.countplot('DAY_OF_WEEK', 'Crimes per Day')

    plotter.countplot('DISTRICT', 'Crimes per District')

    # Question No.2
    plotter.countplot('YEAR', 'Shootings per Year', predicate=lambda data: data['SHOOTING'] == 'Y')

    plotter.countplot('DISTRICT', 'Shootings per District', predicate=lambda data: data['SHOOTING'] == 'Y')

    # Question No.3
    plotter.countplot('TIME_PERIOD', 'Crimes per Time Period')

    # Question No.4
    plotter.countplot('OFFENSE_CODE_GROUP', 'Most Frequent Type Of Crime During The Day', predicate=lambda data: data['TIME_PERIOD'] == 'Day', squeeze=True)

