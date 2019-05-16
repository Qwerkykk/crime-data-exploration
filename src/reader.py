
import pandas as pd

class Reader:

    headers = {
        'INCIDENT_NUMBER': str,
        'OFFENSE_CODE_GROUP': str,
        'DISTRICT': str,
        'SHOOTING': str,
        'YEAR': int,
        'MONTH': int,
        'DAY_OF_WEEK': str,
        'HOUR': int,
        'Lat': float,
        'Long': float
    }

    def __init__(self, filename):

        if not isinstance(filename, str):
            raise ValueError("'filename' is not an instance of 'str'")

        print('<LOG>: Processing file', "'" + filename + "'")

        self.data = pd.read_csv(filename, dtype=self.headers, skipinitialspace=True, usecols=self.headers.keys())

        print('<LOG>:', len(self.data.index), 'rows')

        self.data['SHOOTING'] = [False if value == pd.NaT else True for value in list(self.data['SHOOTING'])]

        print('<LOG>: Dropping NaN values')

        self.data.dropna(inplace=True)

        print('<LOG>:', len(self.data.index), 'rows')

        self.data['TIME_OF_DAY'] = ['DAY' if hour >= 6 and hour <= 18 else 'NIGHT' for hour in list(self.data['HOUR'])]


    def groupby(self, header):

        if not isinstance(header, str):
            raise ValueError("'header' must be an instance of 'str'")

        if not header in self.headers:
            raise ValueError("'" + header + "' is not supported")

        return self.data.groupby(header)


if __name__ == "__main__":

    reader = Reader('../data/crime.csv')

    print(reader.groupby('SHOOTING'))

