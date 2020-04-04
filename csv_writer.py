import csv


class CSVWriter:

    def __init__(self):
        self.file_handler = None
        self.csv_writer = None

    def open(self, file_name):
        self.file_handler = open("out/" + file_name, 'w')
        self.csv_writer = csv.writer(self.file_handler, delimiter=';')
        self.write_row(['time', 'delta', 'modifier', 'keys'])

    def write_row(self, row):
        if self.csv_writer is not None:
            self.csv_writer.writerow(row)

    def close(self):
        if self.file_handler is not None:
            self.file_handler.close()
