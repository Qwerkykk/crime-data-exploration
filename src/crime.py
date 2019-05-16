
from reader import Reader
from visualizer import Visualizer

if __name__ == "__main__":

    reader = Reader('../data/crime.csv')

    # Question No.1
    visualizer = Visualizer(reader)

    visualizer.countplot('YEAR', 'Crimes per Year')

    visualizer.countplot('MONTH', 'Crimes per Month')

    visualizer.countplot('DAY_OF_WEEK', 'Crimes per Day')

    visualizer.countplot('DISTRICT', 'Crimes per District')

    # Question No.2
    visualizer.countplot('YEAR', 'Shootings per Year', predicate=lambda data: data['SHOOTING'] == 'Y')

    visualizer.countplot('DISTRICT', 'Shootings per District', predicate=lambda data: data['SHOOTING'] == 'Y')

    # Question No.3
    visualizer.countplot('TIME_PERIOD', 'Crimes per Time Period')

    # Question No.4
    visualizer.countplot('OFFENSE_CODE_GROUP', 'Most Frequent Type Of Crime During The Day', predicate=lambda data: data['TIME_PERIOD'] == 'Day', squeeze=True)

