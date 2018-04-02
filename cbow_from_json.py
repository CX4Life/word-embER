import json
import string
import re
import glob

def big_string_from_list(list_of_narratives):
    def replace_whitespace(s):
        exclude = set(string.whitespace)
        clean = ''.join([ch if ch not in exclude else ' ' for ch in s])
        return re.sub(' +', ' ', clean).lower()

    def remove_undefined(s):
        include_only = set(string.printable)
        clean = ''.join([ch if ch in include_only else '' for ch in s])
        return clean.lower()

    def apply_cleaning(s):
        return remove_undefined(replace_whitespace(s))

    return ' '.join([apply_cleaning(x) for x in list_of_narratives])


def all_accounts_narratives():
    bag_of_words = []
    for json_filename in glob.glob('*checkpoint.json'):
        with open(json_filename, 'r') as json_file:
            list_of_narratives = json.load(json_file)
        bag_of_words.append(big_string_from_list(list_of_narratives))


    huge_bag = ' '.join(bag_of_words)
    print('How many words?', len(huge_bag.split(' ')))
    return huge_bag


if __name__ == '__main__':
    cbow = all_accounts_narratives()
    with open('cbow.txt', 'w') as out:
        out.write(cbow)
