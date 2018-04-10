import numpy as np
from cbow_from_json import apply_cleaning_to_string

EMBEDDING_LOOKUP_FILENAME = 'embedding_lookup.npy'
UNKNOWN_TOKEN = 'UNK'


def load_lookup():
    """Loads embedding lookup file. For ease of use, returns a Python dictionary"""
    py_dict = {}
    np_lookup = np.load(EMBEDDING_LOOKUP_FILENAME)
    for key in np_lookup.item().keys():
        py_dict[key] = np_lookup.item().get(key)
    return py_dict


def create_vector_set_from_string(input_string, vector_lookup=None):
    """Return 2d numpy array of word embeddings for a string"""

    if vector_lookup is None:
        vector_lookup = load_lookup()

    cleaned = apply_cleaning_to_string(input_string)
    vector_list = []
    for word in cleaned.split(' '):
        try:
            vector_list.append(vector_lookup[word])
        except KeyError:
            vector_list.append(vector_lookup[UNKNOWN_TOKEN])
    return np.array(vector_list)


def string_to_aggregate_vector(string):
    """ Given a string, return a 1-dimensional numpy vector of length 300,
        which is an aggregate of all word embeddings for that string. """
    two_d_nparray = create_vector_set_from_string(string)
    return np.sum(two_d_nparray, axis=0)


def main():
    from scipy.spatial.distance import cosine
    import json
    with open('json/cosine_samples.json') as cs_samples:
        list_of_samples = json.load(cs_samples)
    test_string_good = list_of_samples[0]
    test_string_related = list_of_samples[1]
    test_string_unrelated = list_of_samples[2]
    test_string_nonsense = list_of_samples[3]

    word_to_embedding = load_lookup()

    test_vector_set = create_vector_set_from_string(test_string_good, word_to_embedding)
    tv_related = create_vector_set_from_string(test_string_related, word_to_embedding)
    test_vector_set_bad = create_vector_set_from_string(test_string_unrelated, word_to_embedding)
    tv_vb = create_vector_set_from_string(test_string_nonsense)

    first_sum = np.sum(test_vector_set, axis=0)
    related_sum = np.sum(tv_related, axis=0)
    bad_sum = np.sum(test_vector_set_bad, axis=0)
    vb_sum = np.sum(tv_vb, axis=0)

    dist_out_ident = 1 - cosine(first_sum, first_sum)
    dist_out_sim = 1 - cosine(first_sum, related_sum)
    dist_out_dissim = 1 - cosine(first_sum, bad_sum)
    dist_out_vb = 1 - cosine(first_sum, vb_sum)

    print('Identity cos:   {}\nRelated cos:    {}\nUnrelated mean: {}\nNonsense cos:   {}'.format(dist_out_ident, dist_out_sim, dist_out_dissim, dist_out_vb))


if __name__ == '__main__':
    main()
