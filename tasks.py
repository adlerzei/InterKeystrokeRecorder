from termcolor import colored
import key_pair_generator as keygen
from csv_writer import CSVWriter
import random
import readchar
import recorder
import time


def wait_for_enter():
    while True:
        typed_char = readchar.readkey()
        if typed_char == readchar.key.ENTER:
            break


def filter_buffer(string, packet_buffer):
    if len(packet_buffer) == 0:
        return packet_buffer
    first_key = string[0]
    filtered_buffer = packet_buffer.copy()
    while first_key not in filtered_buffer[0][3]:
        del filtered_buffer[0]
    return filtered_buffer


def is_good_input(packet_buffer):
    for packet in packet_buffer:
        if packet[1].microseconds < 5000:
            return False
    return True


def tuple_to_string(keys):
    string = ""
    for char in keys:
        string += char
    return string


def write_buffer_as_csv(csv_writer, packet_buffer):
    if not csv_writer.is_open:
        return False
    for packet in packet_buffer:
        csv_writer.write_row(packet)
    return True


def get_file_name(user_id, task_id):
    return str(user_id) + "_" + str(task_id)


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

        self.lng = lng
        self.recorder = recorder
        self.csv_writer = CSVWriter()
        self.user_id = random.randint(1000, 9999)

    def welcome_task(self):
        print(self.lng.welcome_ascii)
        print()
        print(self.lng.welcome)
        print()
        print(self.lng.user_id + str(self.user_id) + " " + self.lng.please_note_user_id)
        print()

    def task_1(self):
        if self.csv_writer.is_open:
            self.csv_writer.close()
        self.csv_writer.open(self.user_id, get_file_name(self.user_id, 1))
        print(self.lng.task1_begin)
        readchar.readkey()
        print()
        print(self.lng.task1_ascii)
        print()
        print(self.lng.task1_introduction)
        char_pairs = keygen.get_char_pairs()
        char_count = 0
        for chars in char_pairs:
            progress = round(char_count/len(char_pairs) * 100, 1)
            print()
            print(self.lng.task_general_progress + str(progress) + " %")
            print(self.lng.task1_mission + colored(str(chars), "green"))
            print(self.lng.task_general_hint)
            i = 1
            while i < 31:
                success = self.key_pair_input(chars, i)
                if success:
                    i += 1
            char_count += 1
            print()
        print()
        self.csv_writer.close()

    def task_2(self):
        if self.csv_writer.is_open:
            self.csv_writer.close()
        self.csv_writer.open(self.user_id, get_file_name(self.user_id, 2))
        print(self.lng.task2_begin)
        readchar.readkey()
        print()
        print(self.lng.task2_ascii)
        print()
        print(self.lng.task2_introduction)
        print()
        print(self.lng.task2_hint)
        char_pairs = keygen.get_shift_pairs()
        char_count = 0
        for chars in char_pairs:
            progress = round(char_count / len(char_pairs) * 100, 1)
            print()
            print(self.lng.task_general_progress + str(progress) + " %")
            print(self.lng.task2_mission + colored(str(chars), "green"))
            print(self.lng.task_general_hint)
            i = 1
            while i < 31:
                success = self.key_pair_input(chars, i)
                if success:
                    i += 1
            char_count += 1
            print()
        print()
        self.csv_writer.close()

    def task_3(self, words):
        if self.csv_writer.is_open:
            self.csv_writer.close()
        self.csv_writer.open(self.user_id, get_file_name(self.user_id, 3))
        print(self.lng.task3_begin)
        readchar.readkey()
        print()
        print(self.lng.task3_ascii)
        print()
        print(self.lng.task3_introduction)
        i = 0
        while i < len(words):
            progress = round(i/len(words) * 100, 1)
            print()
            print(self.lng.task_general_progress + str(progress) + " %")
            print(self.lng.task3_mission + colored(words[i], "green"))
            success = self.string_input(words[i])
            if not success:
                print()
                print(self.lng.task3_wrong_input + " " + self.lng.task_general_continue)
                wait_for_enter()
                continue
            i += 1
            print()
        print()
        self.csv_writer.close()

    def task_4(self, passwords):
        if self.csv_writer.is_open:
            self.csv_writer.close()
        self.csv_writer.open(self.user_id, get_file_name(self.user_id, 4))
        print(self.lng.task4_begin)
        readchar.readkey()
        print()
        print(self.lng.task4_ascii)
        print()
        print(self.lng.task4_introduction)
        pw_count = 0
        for pw in passwords:
            progress = round(pw_count/len(passwords) * 100, 1)
            print()
            print(self.lng.task_general_progress + str(progress) + " %")
            print(self.lng.task4_mission + colored(pw, "green"))
            print()
            print(self.lng.task4_get_familiar)
            wait_for_enter()
            print()
            i = 1
            while i < 6:
                success = self.string_input(pw, i)
                if not success:
                    wait_for_enter()
                    continue
                i += 1
            pw_count += 1
            print()
        print()
        self.csv_writer.close()

    def task_5(self, passwords):
        if self.csv_writer.is_open:
            self.csv_writer.close()
        self.csv_writer.open(self.user_id, get_file_name(self.user_id, 5))
        print(self.lng.task5_begin)
        readchar.readkey()
        print()
        print(self.lng.task5_ascii)
        print()
        print(self.lng.task5_introduction)
        pw_count = 0
        for pw in passwords:
            progress = round(pw_count/len(passwords) * 100, 1)
            print()
            print(self.lng.task_general_progress + str(progress) + " %")
            print(self.lng.task5_mission + colored(pw, "green"))
            print()
            print(self.lng.task5_get_familiar)
            wait_for_enter()
            print()
            i = 1
            while i < 6:
                success = self.string_input(pw, i)
                if not success:
                    print()
                    print(self.lng.task5_wrong_input + " " + self.lng.task_general_continue)
                    wait_for_enter()
                    continue
                i += 1
            pw_count += 1
            print()
        print()
        self.csv_writer.close()

    def key_pair_input(self, chars, i):
        self.recorder.clear_packet_buffer()

        print(self.lng.task_general_input + " " + str(i) + ": " + " (0/2)", end="\r")
        first_char = readchar.readkey()
        print(self.lng.task_general_input + " " + str(i) + ": " + " (1/2)", end="\r")
        second_char = readchar.readkey()
        print(self.lng.task_general_input + " " + str(i) + ": " + " (2/2)", end="\r")
        if (first_char, second_char) != chars:
            print(self.lng.task1_wrong_input)
            return False

        time.sleep(0.2)
        filtered_buffer = filter_buffer(tuple_to_string(chars), self.recorder.packet_buffer)
        if not is_good_input(filtered_buffer):
            print(self.lng.task_general_recording_error)
            return False

        return write_buffer_as_csv(self.csv_writer, filtered_buffer)

    def string_input(self, word, i=0):
        self.recorder.clear_packet_buffer()

        typed_word = ""
        if i == 0:
            print(self.lng.task_general_input + ": " + "        ", end="\r")
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
                print(self.lng.task4_wrong_input + " " + self.lng.task_general_continue)
                return False

        time.sleep(0.2)
        filtered_buffer = filter_buffer(word, self.recorder.packet_buffer)
        if not is_good_input(filtered_buffer):
            print()
            print(self.lng.task_general_recording_error + " " + self.lng.task_general_continue)
            return False

        return write_buffer_as_csv(self.csv_writer, filtered_buffer)
