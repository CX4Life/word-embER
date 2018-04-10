import numpy as np
from string_to_embeddings import load_lookup
from string_to_embeddings import string_to_aggregate_vector

CANONCIAL_NARRATIVE_VECTOR_FILENAME = 'canonvect.npy'

def get_high_norm_words(num_to_return, as_percentage=False):
    embedding_lookup = load_lookup()
    if as_percentage:
        num_to_return = (len(embedding_lookup) * num_to_return) // 100
    norm_word_pairs = []
    for key in embedding_lookup.keys():
        norm_word_pairs.append(
            (np.linalg.norm(embedding_lookup[key]), key)
        )
    norm_word_pairs.sort(reverse=True)
    return [pair[1] for pair in norm_word_pairs[:num_to_return]]


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


if __name__ == '__main__':
    test_string = 'While in service for fuel Engine-31 heard a report of a vehicle fire at building 20190; Engine-41 was being dispatched to this emergency. Engine-31 lieutenant asked Chief-1 if he wanted Engine-41 to stand down due to Engine-31 being closer to the incident. Chief-1 approved and Engine-31 was dispatched to the incident. Firefighters donned all protective structural fire equipment and responded to the address. Chief 1 also responded to this incident. Crew arrived on scene, established command, and confirmed there was no active fire. Further investigation revealed the soldiers working on the vehicle utilized a 10-pound Class ABC extinguisher to extinguish the fire. Thermal imager camera was utilized by fire crew and confirmed no hot spots or active fire. Chief-1 arrived on scene and was briefed on the findings. Soldiers on scene stated the fire started under the crew chief side seat. (Possibly due to the alternator). They also secured main power to the vehicle to prevent further damage. Soldiers started complaining of irritation to their eyes and throat; dispatch was advised to notify EMS and have a unit respond. In the meantime, soldiers were escorted to an eye wash station inside the warehouse to flush out their eyes. Medic-5 arrived on scene and was briefed on the patients. Patients refused further medical treatment. Emergency was terminated for Engine-31, Chief-1, and Medic-5. End report.'
    print(compute_is_valid_narrative(test_string))
    import json
    with open('json/cosine_samples.json') as cs_samples:
        list_of_samples = json.load(cs_samples)
    test_string_good = list_of_samples[0]
    test_string_related = list_of_samples[1]
    test_string_unrelated = list_of_samples[2]
    test_string_nonsense = list_of_samples[3]

    print(compute_is_valid_narrative(test_string_good))
    print(compute_is_valid_narrative(test_string_related))
    print(compute_is_valid_narrative(test_string_unrelated))
    print(compute_is_valid_narrative(test_string_nonsense))