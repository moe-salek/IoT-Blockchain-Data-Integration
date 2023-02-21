import csv


def read_csv_data_loop(file):
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        while True:
            for row in reader:
                yield dict(zip(header, row))
            csv_file.seek(0)
