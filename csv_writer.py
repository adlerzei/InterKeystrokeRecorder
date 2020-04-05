import csv
import os
import atexit


class CSVWriter:

    def __init__(self):
        self.file_handler = None
        self.csv_writer = None
        self.is_open = True
        atexit.register(self.close)

    def open(self, user_id, file_name):
        if not os.path.exists("out/" + str(user_id) + "/"):
            os.makedirs("out/" + str(user_id) + "/")

        self.file_handler = open("out/" + str(user_id) + "/" + file_name, 'w')
        self.csv_writer = csv.writer(self.file_handler, delimiter=';')
        self.is_open = True
        self.write_row(['time', 'delta', 'modifier', 'keys'])

    def write_row(self, row):
        if self.csv_writer is not None:
            self.csv_writer.writerow(row)

    def close(self):
        if self.file_handler is not None:
            self.file_handler.close()
            self.is_open = False
