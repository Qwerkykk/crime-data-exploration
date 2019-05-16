
import pandas as pd

class Reader:

    headers = [
        'INCIDENT_NUMBER',
        'OFFENSE_CODE_GROUP',
        'DISTRICT',
        'SHOOTING',
        'YEAR',
        'MONTH',
        'DAY_OF_WEEK',
        'HOUR',
        'Lat',
        'Long'
    ]

    types = dict(zip(headers, [str, str, str, str, int, int, str, int, float, float]))

    def __init__(self, filename):

        if not isinstance(filename, str):
            raise ValueError("'filename' is not an instance of 'str'")

        print('<LOG>: Processing file', "'" + filename + "'")

        self.data = pd.read_csv(filename, dtype=self.types, skipinitialspace=True, usecols=self.headers)

        print('<LOG>:', len(self.data.index), 'rows')

        self.data['SHOOTING'].fillna('N', inplace=True)

        print('<LOG>: Dropping NaN values')

        self.data.dropna(inplace=True)

        print('<LOG>:', len(self.data.index), 'rows')

        self.data['TIME_OF_DAY'] = ['DAY' if hour >= 6 and hour <= 18 else 'NIGHT' for hour in list(self.data['HOUR'])]


    def groupby(self, headers):

        if isinstance(headers, str):
            headers = set([headers])
        elif isinstance(headers, list):
            headers = set(headers)
        else:
            raise ValueError("'headers' must be an instance of 'list'")

        if not headers.issubset(self.headers):
            raise ValueError(headers.difference(self.headers), 'header(s) are not supported')

        return self.data.groupby(list(headers))


if __name__ == "__main__":

    reader = Reader('../data/crime.csv')

    print(reader.groupby(['SHOOTING']))

