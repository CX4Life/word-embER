# word-embER
### Train word embeddings from ER's narrative text.

### Motivation

Word embeddings are a useful tool in the realm of natural language processing and deep learning.
Word embeddings are vectors which represent words in a high dimensional vector space, and
which capture the context and meaning of those words in the context of their usage. For more
information on word embeddings,
[see this Tensorflow tutorial](https://www.tensorflow.org/tutorials/word2vec).

Access to pre-trained word embeddings expedites natural language research, however because
word embeddings are sensitive to the context in which words are used, the corpus from which
word embeddings are trained affects their usefulness. Embeddings trained from news articles
are readily available, but no set of embeddings trained from emergency data exists.

Finally, these embeddings can be used to examine and characterize our own narrative data at
Emergency Reporting! This is the cool part.

### Installation
`git clone this here repo`

A virtualenv may be helpful - 64-bit Python 3.5 or 3.6 is the required is the
required interpreter due to Tensorflow's requirements.

`pip install -r requirements.txt`

### History
- 4.8.18 Used example word2vec to train embeddings after a long time trying to scratch
build a model. Uploaded sample .npy file where order of rows corresponds to the rank
of each word in rank2word.json. Plot shows cosine similarity of words. Of note, embeddings
created with window size of 5, i.e. `[context, context, target, context, context]` for
evaluation of each target word embedding.

- 4.2.18 Making tons of API requests for data - interestingly, a lot
of accounts that have 10's or 100's of thousands of incidents also
haven't written a single narrative. Data is cleaned to be without punctuation,
all lowercase. Certain accounts with a large number of narratives may upset
the count of frequent words, because the proper nouns they use end up appearing
frequently enough to upset the contexts of other words.

- 3.28.18 Initial commit, begin scraper

### License - MIT
