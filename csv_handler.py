import csv
import os


class CSVHandler:

    def __init__(self):
        self.path = ""
        self.file_name = ""

    def set_path_and_file_name(self, path, file_name):
        self.path = path
        self.file_name = file_name

    def make_path_and_file(self, file_name, user_id="", task_id="", string_to_enter=""):
        data_file = False
        if user_id == "" and task_id == "" and string_to_enter == "":
            path = "out/"
        elif task_id == "" and string_to_enter == "":
            path = "out/" + str(user_id) + "/"
        elif string_to_enter == "":
            path = "out/" + str(user_id) + "/" + str(task_id) + "/"
            data_file = True
        else:
            path = "out/" + str(user_id) + "/" + str(task_id) + "/" + string_to_enter + "/"
            data_file = True

        if not os.path.exists(path):
            os.makedirs(path)

        self.set_path_and_file_name(path, file_name)

        if data_file:
            with open(self.path + "/" + self.file_name, 'w') as f:
                csv_writer = csv.writer(f, delimiter=';')
                csv_writer.writerow(['i',
                                     'delta',
                                     'sniff-intervals',
                                     'modifier-scan-code',
                                     'keys-scan-code',
                                     'modifier',
                                     'keys'])
        else:
            open(self.path + "/" + self.file_name, 'a+')

    def write_row(self, row):
        with open(self.path + "/" + self.file_name, 'a+') as f:
            csv_writer = csv.writer(f, delimiter=';')
            csv_writer.writerow(row)

    def read_csv_to_dict(self):
        with open(self.path + self.file_name, mode='r') as f:
            reader = csv.reader(f, delimiter=";")
            return dict((str(rows[0]), str(rows[1])) for rows in reader)

    def read_csv_to_list(self):
        with open(self.path + self.file_name, mode='r') as f:
            reader = csv.reader(f, delimiter=";")
            return list(reader)
