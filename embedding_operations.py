import numpy as np
from string_to_embeddings import load_lookup
from string_to_embeddings import string_to_aggregate_vector

CANONCIAL_NARRATIVE_VECTOR_FILENAME = 'numpy_arrays/canonvect.npy'


def sort_word_embeddings_by_norm():
    embedding_lookup = load_lookup()
    norm_word_pairs = []
    for key in embedding_lookup.keys():
        norm_word_pairs.append(
            (np.linalg.norm(embedding_lookup[key]), key)
        )
    norm_word_pairs.sort(reverse=True)
    return norm_word_pairs


def get_high_norm_words(num_to_return, as_percentage=False):
    norm_word_pairs = sort_word_embeddings_by_norm()
    if as_percentage:
        num_to_return = (len(norm_word_pairs) * num_to_return) // 100

    return [pair[1] for pair in norm_word_pairs[:num_to_return]]


def get_central_norm_words(num_to_return, as_percent=False):
    norm_word_pairs = sort_word_embeddings_by_norm()

    if as_percent:
        num_to_return = (len(norm_word_pairs) * num_to_return) // 100

    mid_point = len(norm_word_pairs) // 2
    low_bound = mid_point - (num_to_return // 2)
    hi_bound = mid_point + (num_to_return // 2)

    return [pair[1] for pair in norm_word_pairs[low_bound:hi_bound]]


def get_top_n_words(num_words, string, limited_set=None):
    """Attempt was to extract subject from text, but near origin vectors are too similar..."""
    from scipy.spatial.distance import cosine
    aggregate_vector = string_to_aggregate_vector(string)
    embedding_lookup = load_lookup()
    all_word_cosine_pairs = []
    if limited_set is None:
        for key in embedding_lookup.keys():
            distance = 1 - cosine(embedding_lookup[key], aggregate_vector)
            all_word_cosine_pairs.append((distance, key))
    else:
        limited_set = set(limited_set)
        for key in embedding_lookup.keys():
            if key in limited_set:
                distance = 1 - cosine(embedding_lookup[key], aggregate_vector)
                all_word_cosine_pairs.append((distance, key))
    all_word_cosine_pairs.sort(reverse=True)
    return [pair[1] for pair in all_word_cosine_pairs[:num_words]]


def get_string_similarity(s_one, s_two):
    from scipy.spatial.distance import cosine
    embedding_one = string_to_aggregate_vector(s_one)
    embedding_two = string_to_aggregate_vector(s_two)
    return 1 - cosine(embedding_one, embedding_two)


def compute_is_valid_narrative(given_narrative):
    from scipy.spatial.distance import cosine

    def maybe_create_prototypical_narrative_vector():
        from os import path
        if not path.isfile(CANONCIAL_NARRATIVE_VECTOR_FILENAME):
            import json

            with open('bag_of_ranks.json', 'r') as rank_file:
                ranks = json.load(rank_file)
            with open('rank2word.json', 'r') as dict_file:
                converter = json.load(dict_file)
            shockingly_bad = [converter[str(rank)] for rank in ranks]
            vectors = []
            chunk = len(shockingly_bad) // 1000
            for i in range(1000):
                if i % 100 == 0:
                    print('-')
                so_bad = ' '.join(shockingly_bad[chunk * i: chunk * (i + 1)])
                vectors.append(string_to_aggregate_vector(so_bad))
            enormous_vector = np.sum(vectors)
            np.save(CANONCIAL_NARRATIVE_VECTOR_FILENAME, enormous_vector)
            return enormous_vector
        else:
            return np.load(CANONCIAL_NARRATIVE_VECTOR_FILENAME)

    this_narrative_vector = string_to_aggregate_vector(given_narrative)
    canon_vector = maybe_create_prototypical_narrative_vector()
    return cosine(this_narrative_vector, canon_vector)


def score_string_set(num_subject_words, subect_wordset, list_of_strings):

    def first_ten_words(string):
        return ' '.join(string.split(' ')[:10])

    results = []
    for string in list_of_strings:
        results.append({
            'String': first_ten_words(string),
            #'Confidence': compute_is_valid_narrative(string),
            'Subjects': get_top_n_words(num_subject_words, string, subect_wordset)
        })
    return results


if __name__ == '__main__':
    central_words = get_central_norm_words(20, as_percent=True)
    import json
    import pprint
    with open('json/cosine_samples.json') as cs_samples:
        list_of_samples = json.load(cs_samples)
    pp = pprint.PrettyPrinter(indent=2, width=100)
    pp.pprint(score_string_set(5, central_words, list_of_samples))
