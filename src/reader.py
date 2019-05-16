
import csv

class Reader:

    headers = {
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
    }

    transform = { header: lambda entry: entry for header in headers }

    transform['SHOOTING'] = lambda entry: True if entry else False
    transform['YEAR']     = lambda entry: int(entry)
    transform['MONTH']    = lambda entry: int(entry)
    transform['HOUR']     = lambda entry: int(entry)
    transform['Lat']      = lambda entry: float(entry)
    transform['Long']     = lambda entry: float(entry)

    def __init__(self, filename):

        self.columns = { key : [] for key in self.headers }

        with open(filename, 'r', encoding='ascii', errors='ignore') as file:

            reader = csv.reader(file)

            headers = list(map(lambda s: s.strip(), list(next(reader, None))))

            indices = { index : header for index, header in enumerate(headers) if header in self.columns.keys() }

            total, skipped = 0, 0

            for row in reader:
                total += 1
                row = list(map(str.strip, row))

                for index in range(len(row)):
                    if index in indices.keys():
                        header = indices[index]
                        entry  = self.transform[header](row[index])
                        self.columns[header].append(entry)

            if skipped:
                print("<LOG>:", skipped, "out of", total, "lines skipped")


    def group_by(self, header):

        if not isinstance(header, str):
            raise ValueError("'header' must be an instance of 'str'")

        if not header in self.headers:
            raise ValueError("'" + header + "' is not supported")

        groups = {}

        for id, value in zip(self.columns['INCIDENT_NUMBER'], self.columns[header]):
            if not value in groups:
                groups[value] = []

            groups[value].append(id)

        return groups


if __name__ == "__main__":

    reader = Reader('../data/head.csv')

    print(reader.group_by('SHOOTING'))

