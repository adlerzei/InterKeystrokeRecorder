import key_pair_generator as keygen
import readchar


def wait_for_enter():
    while True:
        typed_char = readchar.readkey()
        if typed_char == readchar.key.ENTER:
            break


class TaskGenerator:
    def __init__(self, locale='e'):
        if locale == 'g':
            self.lng = __import__("data_study_DE")
        else:
            self.lng = __import__("data_study_EN")

    def task_1(self, chars):
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
            print(self.lng.task1_mission + str(chars))
            print(self.lng.task_general_hint)
            i = 1
            while i < 31:
                success = self.key_pair_input(chars, i)
                if success:
                    i += 1
            char_count += 1
            print()
        print()

    def task_2(self, chars):
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
            print(self.lng.task2_mission + str(chars))
            print(self.lng.task_general_hint)
            i = 1
            while i < 31:
                success = self.key_pair_input(chars, i)
                if success:
                    i += 1
            char_count += 1
            print()
        print()

    def task_3(self, words):
        print(self.lng.task2_begin)
        readchar.readkey()
        print()
        print(self.lng.task2_ascii)
        print()
        print(self.lng.task2_introduction)
        i = 0
        while i < len(words):
            progress = round(i/len(words) * 100, 1)
            print()
            print(self.lng.task_general_progress + str(progress) + " %")
            print(self.lng.task2_mission + words[i])
            success = self.string_input(words[i])
            if not success:
                print()
                print(self.lng.task2_wrong_input + " " + self.lng.task_general_continue)
                wait_for_enter()
                continue
            i += 1
            print()
        print()

    def task_4(self, passwords):
        print(self.lng.task3_begin)
        readchar.readkey()
        print()
        print(self.lng.task3_ascii)
        print()
        print(self.lng.task3_introduction)
        pw_count = 0
        for pw in passwords:
            progress = round(pw_count/len(passwords) * 100, 1)
            print()
            print(self.lng.task_general_progress + str(progress) + " %")
            print(self.lng.task3_mission + pw)
            print()
            print(self.lng.task3_get_familiar)
            wait_for_enter()
            print()
            i = 1
            while i < 6:
                success = self.string_input(pw, i)
                if not success:
                    print()
                    print(self.lng.task2_wrong_input + " " + self.lng.task_general_continue)
                    wait_for_enter()
                    continue
                i += 1
            pw_count += 1
            print()
        print()

    def key_pair_input(self, chars, i):
        print(self.lng.task_general_input + " " + str(i) + ": " + " (0/2)", end="\r")
        first_char = readchar.readkey()
        print(self.lng.task_general_input + " " + str(i) + ": " + " (1/2)", end="\r")
        second_char = readchar.readkey()
        print(self.lng.task_general_input + " " + str(i) + ": " + " (2/2)", end="\r")
        if (first_char, second_char) != chars:
            print(self.lng.task1_wrong_input)
            return False
        else:
            return True

    def string_input(self, word, i=0):
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
                return False
        return True
