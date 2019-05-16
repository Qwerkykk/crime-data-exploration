
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

    def __init__(self, filename):

        if not isinstance(filename, str):
            raise ValueError("'filename' is not an instance of 'str'")

        print('<LOG>: Loading headers', self.headers)

        self.data = pd.read_csv(filename, skipinitialspace=True, usecols=self.headers)

        print('<LOG>:', len(self.data.index), 'rows [Before dropping NaN values]')

        self.data['SHOOTING'].fillna('N', inplace=True)

        self.data.dropna()

        print('<LOG>:', len(self.data.index), 'rows [After dropping NaN values]')

        self.data['TIME_OF_DAY'] = ['DAY' if hour >= 6 and hour <= 18 else 'NIGHT' for hour in list(self.data['HOUR'])]


    def groupby(self, header):

        if not isinstance(header, str):
            raise ValueError("'header' must be an instance of 'str'")

        if not header in self.headers:
            raise ValueError("'" + header + "' is not supported")

        return self.data.groupby(header)


if __name__ == "__main__":

    reader = Reader('../data/head.csv')

    print(reader.groupby('SHOOTING'))

