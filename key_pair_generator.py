import random
import config


def get_char_pairs():
    random.seed(config.random_seed)

    all_char_pairs = get_all_possible_char_pairs(config.chars)
    char_pairs = []

    # fill char pairs with needed char pairs from words
    for word in config.words:
        last_char = ""
        for char in word:
            if last_char == "":
                last_char = char
            else:
                if (last_char, char) not in char_pairs:
                    char_pairs.append((last_char, char))
                last_char = char

    # fill char pairs with needed char pairs from pws
    for pw in config.passwords:
        last_char = ""
        for char in pw:
            if last_char == "":
                last_char = char
            else:
                if (last_char, char) not in char_pairs:
                    char_pairs.append((last_char, char))
                last_char = char

    # fill up char pairs up to a length of 142 with random char pairs from chars
    i = 0
    need_key_pair_count = 142-len(char_pairs)
    while i < need_key_pair_count:
        pair_to_test = all_char_pairs[random.randint(0, len(all_char_pairs)-1)]
        if str.isdigit(str(pair_to_test[0])) and str.isdigit(str(pair_to_test[1])):
            continue

        if pair_to_test in char_pairs:
            continue

        char_pairs.append(pair_to_test)
        i += 1

    return char_pairs


def get_shift_pairs():
    random.seed(config.random_seed)
    alpha_chars = list(filter(lambda x: str.isalpha(x), config.chars))
    shift_pairs = []

    for char in config.chars:
        if str.isalpha(char):
            i = random.randint(0, len(alpha_chars) - 1)
            if char != alpha_chars[i]:
                shift_pairs.append((char, str.upper(alpha_chars[i])))
                del alpha_chars[i]
    return shift_pairs


def get_all_possible_char_pairs(chars):
    all_char_pairs = []

    # generate all possible key pairs
    for first_char in chars:
        for second_char in chars:
            if (first_char, second_char) not in all_char_pairs:
                all_char_pairs.append((first_char, second_char))

    return all_char_pairs


# print(get_char_pairs())
# print(get_shift_pairs())
