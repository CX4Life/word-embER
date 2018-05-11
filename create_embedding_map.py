import json
import numpy as np

JSON_DIR = 'json/'
NPARRAY_DIR = 'numpy_arrays/'


def load_rank_map():
    with open(JSON_DIR + 'rank2word.json') as rank_map_file:
        rank_map = json.load(rank_map_file)
    return rank_map


def load_embeddings_list():
    embeddings = np.load(NPARRAY_DIR + 'embeddings.npy')
    print(embeddings.shape)
    return embeddings


def create_embedding_map(dictionary, embeddings):
    word_embedding_map = {}
    for rank, row in enumerate(embeddings):
        word = dictionary[str(rank)]
        print(word)
        word_embedding_map[word] = row

    return word_embedding_map


def main():
    ranks_to_words = load_rank_map()
    embeddings = load_embeddings_list()
    string_to_ndarray_map = create_embedding_map(ranks_to_words, embeddings)
    np.save(NPARRAY_DIR + 'embedding_lookup.npy', string_to_ndarray_map)


if __name__ == '__main__':
    main()
