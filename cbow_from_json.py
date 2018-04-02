import json
import string
import re
import glob

__author__ = 'Tim Woods'
__copyright__ = 'Copyright (c) 2018 Tim Woods'
__license__ = 'MIT'

NARRATIVE_DIRECTORY = 'narrative_files/'

def big_string_from_list(list_of_narratives):
    def replace_whitespace(s):
        exclude = set(string.whitespace)
        return ''.join([ch if ch not in exclude else ' ' for ch in s])

    def remove_undefined(s):
        include_only = set(string.printable)
        clean = ''.join([ch if ch in include_only else '' for ch in s])
        return clean.lower()

    def remove_punctuation_and_digits(s):
        exclude = set(string.punctuation + string.digits)
        return ''.join([ch if ch not in exclude else '' for ch in s.lower()])

    def apply_cleaning(s):
        with_extra_spaces = remove_punctuation_and_digits(remove_undefined(replace_whitespace(s)))
        return re.sub(' +', ' ', with_extra_spaces).lower()

    return ' '.join([apply_cleaning(x) for x in list_of_narratives])


def all_accounts_narratives():
    bag_of_words = []
    for json_filename in reversed(glob.glob(NARRATIVE_DIRECTORY + '*checkpoint.json')):
        with open(json_filename, 'r') as json_file:
            list_of_narratives = json.load(json_file)

        cleaned = big_string_from_list(list_of_narratives)
        bag_of_words.append(cleaned)


    huge_bag = ' '.join(bag_of_words)
    print('How many words?', len(huge_bag.split(' ')))
    return huge_bag


if __name__ == '__main__':
    cbow = all_accounts_narratives()
    with open('cbow.txt', 'w') as out:
        out.write(cbow)
