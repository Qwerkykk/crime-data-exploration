
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

            for row in reader:
                for index in range(len(row)):
                    if index in indices.keys():
                        header = indices[index]
                        entry  = self.transform[header](row[index].strip())
                        self.columns[header].append(entry)


if __name__ == "__main__":

    reader = Reader('../data/head.csv')

    

