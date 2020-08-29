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

from termcolor import colored
from csv_handler import CSVHandler
import sys
import random
import readchar
import recorder
import time
import config


def wait_for_enter():
    while True:
        typed_char = readchar.readkey()
        if typed_char == readchar.key.ENTER:
            break


def filter_buffer_from_string(string, packet_buffer):
    if len(packet_buffer) == 0:
        return packet_buffer
    first_key = string[0]
    filtered_buffer = packet_buffer.copy()
    while filtered_buffer and first_key not in filtered_buffer[0][5]:
        del filtered_buffer[0]
    return filtered_buffer


def filter_buffer_for_shift(string, packet_buffer):
    if len(packet_buffer) == 0:
        return packet_buffer
    first_key = string[0]
    filtered_buffer = packet_buffer.copy()

    if first_key.isupper() or first_key == config.shift:
        while filtered_buffer and filtered_buffer[0][4] != config.shift:
            del filtered_buffer[0]
    else:
        while filtered_buffer and first_key not in filtered_buffer[0][5]:
            del filtered_buffer[0]

    return filtered_buffer


def check_for_modifier(packet_buffer, shift_allowed):
    for packet in packet_buffer:
        if shift_allowed:
            if packet[2] != '02' and packet[2] != '00':
                return False
        else:
            if packet[2] != '00':
                return False
    return True


def check_shift_input(chars, packet_buffer):
    first_key = chars[0]
    contains_shift = False
    contains_char = False
    if first_key.isupper() or first_key == config.shift:
        if first_key.isupper():
            char_to_type = first_key.lower()
        else:
            char_to_type = chars[1]

        if packet_buffer[0][4] == config.shift:
            contains_shift = True
        for i in range(1, len(packet_buffer)):
            if char_to_type in packet_buffer[i][5]:
                contains_char = True
                break
    else:
        if first_key in packet_buffer[0][5]:
            contains_char = True
        for i in range(1, len(packet_buffer)):
            if packet_buffer[i][4] == config.shift:
                contains_shift = True
                break

    return contains_shift and contains_char


def is_good_input(packet_buffer):
    for i in range(1, len(packet_buffer)):
        if packet_buffer[i][0].microseconds < 5000:
            return False
    return True


def tuple_to_string(keys):
    string = ""
    for char in keys:
        string += char
    return string


def write_buffer_as_csv(csv_writer, packet_buffer, i):
    for packet in packet_buffer:
        csv_writer.write_row([i] + packet)


def get_file_name(user_id, task_id, string_to_enter=""):
    if string_to_enter == "":
        return str(user_id) + "_" + str(task_id)
    else:
        return str(user_id) + "_" + str(task_id) + "_" + string_to_enter


class TaskGenerator:
    def __init__(self):
        recorder.start()
        print()

        while True:
            locale = input("Please choose your desired language. Type G for German and E for English: ")
            locale = locale.casefold()
            if locale == 'g' or locale == 'e':
                break

        if locale == 'g':
            import lng.data_study_DE as lng
        else:
            import lng.data_study_EN as lng

        self.locale = locale
        self.lng = lng
        self.recorder = recorder
        self.csv_handler = CSVHandler()
        self.user_id = 0
        self.csv_handler.make_path_and_file(
            config.users_file_name
        )
        self.user_list = list(map(lambda x: x[0], self.csv_handler.read_csv_to_list()))

    def welcome_task(self):
        print(self.lng.welcome_ascii)
        print()
        print(self.lng.welcome)
        print()
        print(self.lng.very_thanks)
        print()
        self.csv_handler.make_path_and_file(
            config.users_file_name
        )

        while self.user_id not in self.user_list:
            while True:
                resume_recording = input(self.lng.resume_old_recording)
                resume_recording = resume_recording.casefold()
                if self.locale == 'g':
                    if resume_recording == 'j' or resume_recording == 'n':
                        break
                else:
                    if resume_recording == 'y' or resume_recording == 'n':
                        break

            if resume_recording == 'n':
                user_id = random.randint(1000, 9999)
                while str(user_id) in self.user_list:
                    user_id = random.randint(1000, 9999)
                self.user_id = user_id
                self.user_list.append(user_id)
                self.csv_handler.write_row([self.user_id])
                print(self.lng.user_id + colored(str(self.user_id), "red") + " " + self.lng.please_note_user_id)
                print()
            else:
                user_id = input(self.lng.enter_user_id)
                if user_id not in self.user_list:
                    print(self.lng.wrong_user_id)
                else:
                    self.user_id = user_id
        print()
        print(self.lng.read_carefully + " " + self.lng.if_help)
        print()

    def task_1(self, char_pairs):
        # get actual task completion status
        task_completion_status = self.get_task_completion_status(1, char_pairs)
        if task_completion_status == config.task_completed:
            return

        print(self.lng.task1_begin)
        readchar.readkey()
        print()
        print(self.lng.task1_ascii)
        print()
        print(self.lng.task1_introduction)
        char_count = 0
        go_to_task_completion = True
        for chars in char_pairs:
            # move forward until current task completion status is reached
            if go_to_task_completion:
                if chars != task_completion_status:
                    char_count += 1
                    continue
                else:
                    go_to_task_completion = False

            # open file to make sure its created
            self.csv_handler.make_path_and_file(
                get_file_name(self.user_id, 1, tuple_to_string(chars)),
                self.user_id,
                1,
                tuple_to_string(chars)
            )

            # get input from user
            progress = round(char_count/len(char_pairs) * 100, 1)
            print()
            print(self.lng.task_general_progress + str(progress) + " %")
            print(self.lng.task1_mission + colored(str(chars), "green"))
            print(self.lng.task_general_hint)
            i = 1
            while i < 31:
                success = self.key_pair_input(chars, config.small_sleep_interval, i)
                if success:
                    i += 1
            char_count += 1
            print()

            # update task completion status
            self.update_task_completion_status(1, chars)
        self.update_task_completion_status(1, config.task_completed)
        print()

    def task_2(self, char_pairs):
        # get actual task completion status
        task_completion_status = self.get_task_completion_status(2, char_pairs)
        if task_completion_status == config.task_completed:
            return

        print(self.lng.task2_begin)
        readchar.readkey()
        print()
        print(self.lng.task2_ascii)
        print()
        print(self.lng.task2_introduction)
        print()
        print(self.lng.task2_hint)
        char_count = 0
        go_to_task_completion = True
        for chars in char_pairs:
            # move forward until current task completion status is reached
            if go_to_task_completion:
                if chars != task_completion_status:
                    char_count += 1
                    continue
                else:
                    go_to_task_completion = False

            # open file to make sure its created
            self.csv_handler.make_path_and_file(
                get_file_name(self.user_id, 2, tuple_to_string(chars)),
                self.user_id,
                2,
                tuple_to_string(chars)
            )

            # get input from user
            progress = round(char_count / len(char_pairs) * 100, 1)
            print()
            print(self.lng.task_general_progress + str(progress) + " %")
            print(self.lng.task2_mission + colored(str(chars), "green"))
            print(self.lng.task_general_hint)
            i = 1
            while i < 31:
                success = self.shift_pair_input(chars, config.long_sleep_interval, i)
                if success:
                    i += 1
            char_count += 1
            print()

            # update task completion status
            self.update_task_completion_status(2, chars)
        self.update_task_completion_status(2, config.task_completed)
        print()

    def task_3(self, words):
        # get actual task completion status
        task_completion_status = self.get_task_completion_status(3, words)
        if task_completion_status == config.task_completed:
            return

        print(self.lng.task3_begin)
        readchar.readkey()
        print()
        print(self.lng.task3_ascii)
        print()
        print(self.lng.task3_introduction)
        i = 0
        go_to_task_completion = True
        while i < len(words):
            # move forward until current task completion status is reached
            if go_to_task_completion:
                if words[i] != task_completion_status:
                    i += 1
                    continue
                else:
                    go_to_task_completion = False

            # get input from user
            self.csv_handler.make_path_and_file(
                get_file_name(self.user_id, 3, words[i]),
                self.user_id,
                3,
                words[i]
            )
            progress = round(i/len(words) * 100, 1)
            print()
            print(self.lng.task_general_progress + str(progress) + " %")
            print(self.lng.task3_mission + colored(words[i], "green"))
            success = self.string_input(words[i], config.small_sleep_interval, False)
            if not success:
                wait_for_enter()
                continue

            # update task completion status
            self.update_task_completion_status(3, words[i])

            i += 1
            print()

        self.update_task_completion_status(3, config.task_completed)
        print()

    def task_4(self, passwords, shift_passwords=None):
        if shift_passwords is not None:
            all_passwords = passwords + shift_passwords
        else:
            all_passwords = passwords

        # get actual task completion status
        task_completion_status = self.get_task_completion_status(4, all_passwords)
        if task_completion_status == config.task_completed:
            return

        print(self.lng.task4_begin)
        readchar.readkey()
        print()
        print(self.lng.task4_ascii)
        print()
        print(self.lng.task4_introduction)
        pw_count = 0
        go_to_task_completion = True
        for pw in all_passwords:
            # move forward until current task completion status is reached
            if go_to_task_completion:
                if pw != task_completion_status:
                    pw_count += 1
                    continue
                else:
                    go_to_task_completion = False

            # get input from user
            self.csv_handler.make_path_and_file(
                get_file_name(self.user_id, 4, pw),
                self.user_id,
                4,
                pw
            )
            progress = round(pw_count/len(all_passwords) * 100, 1)
            print()
            print(self.lng.task_general_progress + str(progress) + " %")
            print(self.lng.task4_mission + colored(pw, "green"))
            print()
            print(self.lng.task4_get_familiar)
            wait_for_enter()
            print()
            i = 1
            while i < 6:
                success = self.string_input(pw, config.small_sleep_interval, pw_count >= len(passwords), i)
                if not success:
                    wait_for_enter()
                    continue
                i += 1
            pw_count += 1
            print()

            # update task completion status
            self.update_task_completion_status(4, pw)
        self.update_task_completion_status(4, config.task_completed)
        print()

    def task_5(self, passwords, shift_passwords=None):
        if shift_passwords is not None:
            all_passwords = passwords + shift_passwords
        else:
            all_passwords = passwords

        # get actual task completion status
        task_completion_status = self.get_task_completion_status(5, all_passwords)
        if task_completion_status == config.task_completed:
            return

        print(self.lng.task5_begin)
        readchar.readkey()
        print()
        print(self.lng.task5_ascii)
        print()
        print(self.lng.task5_introduction)
        pw_count = 0
        go_to_task_completion = True
        for pw in all_passwords:
            # move forward until current task completion status is reached
            if go_to_task_completion:
                if pw != task_completion_status:
                    pw_count += 1
                    continue
                else:
                    go_to_task_completion = False

            # get input from user
            self.csv_handler.make_path_and_file(
                get_file_name(self.user_id, 5, pw),
                self.user_id,
                5,
                pw
            )
            progress = round(pw_count/len(all_passwords) * 100, 1)
            print()
            print(self.lng.task_general_progress + str(progress) + " %")
            print(self.lng.task5_mission + colored(pw, "green"))
            print()
            print(self.lng.task5_get_familiar)
            wait_for_enter()
            print()
            i = 1
            while i < 6:
                success = self.string_input(pw, config.small_sleep_interval, pw_count >= len(passwords), i)
                if not success:
                    wait_for_enter()
                    continue
                i += 1
            pw_count += 1
            print()

            # update task completion status
            self.update_task_completion_status(5, pw)
        self.update_task_completion_status(5, config.task_completed)
        print()

    def goodbye_task(self):
        print(self.lng.task_goodbye_thank_you)
        print()
        print(self.lng.task_goodbye_goodbye)
        print()
        print(self.lng.task_goodbye_quit)
        readchar.readkey()
        sys.exit()

    def get_task_completion_status(self, task_id, input_list):
        self.csv_handler.make_path_and_file(config.completed_tasks_file_name, self.user_id)
        completed_tasks = self.csv_handler.read_csv_to_list()
        if [str(task_id), config.task_completed] in completed_tasks:
            return config.task_completed
        else:
            for to_input in input_list:
                if [str(task_id), str(to_input)] not in completed_tasks:
                    return to_input

    def update_task_completion_status(self, task_id, completion_status):
        self.csv_handler.make_path_and_file(
            config.completed_tasks_file_name,
            self.user_id
        )
        self.csv_handler.write_row([task_id, completion_status])

    def shift_pair_input(self, chars, sleep_interval, i):
        self.recorder.clear_packet_buffer()

        print(self.lng.task_general_input + " " + str(i), end="\r")
        input_char = readchar.readkey()

        if chars[0] == config.shift:
            char_to_compare = chars[1]
        else:
            char_to_compare = chars[0]

        if input_char != char_to_compare:
            print(self.lng.task_general_wrong_input)
            return False

        time.sleep(sleep_interval)
        filtered_buffer = filter_buffer_for_shift(chars, self.recorder.packet_buffer)

        if not filtered_buffer:
            print(self.lng.task_general_wrong_input)
            return False

        if not check_shift_input(chars, filtered_buffer) or not check_for_modifier(filtered_buffer, True):
            print(self.lng.task_general_wrong_input)
            return False

        if not is_good_input(filtered_buffer):
            print(self.lng.task_general_recording_error)
            return False

        write_buffer_as_csv(self.csv_handler, filtered_buffer, i)
        return True

    def key_pair_input(self, chars, sleep_interval, i):
        self.recorder.clear_packet_buffer()

        print(self.lng.task_general_input + " " + str(i) + ": " + " (0/2)", end="\r")
        first_char = readchar.readkey()
        print(self.lng.task_general_input + " " + str(i) + ": " + " (1/2)", end="\r")
        second_char = readchar.readkey()
        print(self.lng.task_general_input + " " + str(i) + ": " + " (2/2)", end="\r")
        if (first_char, second_char) != chars:
            print(self.lng.task_general_wrong_input)
            return False

        time.sleep(sleep_interval)
        filtered_buffer = filter_buffer_from_string(tuple_to_string(chars), self.recorder.packet_buffer)
        if not check_for_modifier(filtered_buffer, False):
            print(self.lng.task_general_wrong_input)
            return False

        if not is_good_input(filtered_buffer):
            print(self.lng.task_general_recording_error)
            return False

        write_buffer_as_csv(self.csv_handler, filtered_buffer, i)
        return True

    def string_input(self, word, sleep_interval, shift_allowed, i=0):
        self.recorder.clear_packet_buffer()
        typed_word = ""

        if i == 0:
            print(self.lng.task_general_input + ": " + "        ", end="\r")
            i = 1
        else:
            print(self.lng.task_general_input + " " + str(i) + ": " + "        ", end="\r")

        for char in word:
            typed_char = readchar.readkey()
            typed_word = typed_word + typed_char
            if i == 0:
                print(self.lng.task_general_input + ": " + typed_word, end="\r")
            else:
                print(self.lng.task_general_input + " " + str(i) + ": " + typed_word, end="\r")
            if typed_char != char:
                print()
                print(self.lng.task_general_wrong_input + " " + self.lng.task_general_continue)
                return False

        time.sleep(sleep_interval)
        if shift_allowed:
            filtered_buffer = filter_buffer_for_shift(word, self.recorder.packet_buffer)
        else:
            filtered_buffer = filter_buffer_from_string(word, self.recorder.packet_buffer)
        if not check_for_modifier(filtered_buffer, shift_allowed):
            print(self.lng.task_general_wrong_input + " " + self.lng.task_general_continue)
            return False

        if not is_good_input(filtered_buffer):
            print()
            print(self.lng.task_general_recording_error + " " + self.lng.task_general_continue)
            return False

        write_buffer_as_csv(self.csv_handler, filtered_buffer, i)
        return True
