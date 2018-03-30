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

A virtualenv may be helpful (more details here)

`pip install -r requirements.txt`

### History
- 3.28.18 Initial commit, begin scraper

### License - MIT
