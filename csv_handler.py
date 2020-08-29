# Copyright (C) 2020  Christian Zei
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
