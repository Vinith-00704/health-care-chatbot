import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer, PorterStemmer

# Download all required NLTK data
for pkg in ['punkt', 'punkt_tab', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']:
    try:
        nltk.download(pkg, quiet=True)
    except Exception:
        pass

_lemmatizer = WordNetLemmatizer()
_stemmer = PorterStemmer()
_stop_words = set(stopwords.words('english')) - {
    'no', 'not', 'nor', 'never', 'nothing', 'without'  # keep negation words
}

# Negation triggers — words that flip symptom meaning
NEGATION_WORDS = {'no', 'not', 'without', 'never', 'none', "don't", "doesn't",
                  "didn't", "can't", "cannot", "haven't", "hasn't"}


def _get_wordnet_pos(treebank_tag):
    """Convert POS tag to WordNet format for better lemmatization."""
    tag_map = {'J': wordnet.ADJ, 'V': wordnet.VERB, 'N': wordnet.NOUN, 'R': wordnet.ADV}
    return tag_map.get(treebank_tag[0], wordnet.NOUN)


def preprocess_text(text: str) -> dict:
    """
    Full NLP preprocessing pipeline.
    Returns:
        dict with keys:
          - 'tokens': clean lemmatized tokens
          - 'stems': stemmed tokens
          - 'original_lower': lowercased original
          - 'negated_zones': list of words preceded by a negation
    """
    original_lower = text.lower().strip()

    # Remove punctuation except apostrophes (for contractions)
    cleaned = re.sub(r"[^a-z0-9\s']", ' ', original_lower)

    # Tokenize
    tokens = word_tokenize(cleaned)

    # POS tagging for smart lemmatization
    try:
        pos_tags = nltk.pos_tag(tokens)
    except Exception:
        pos_tags = [(t, 'NN') for t in tokens]

    # Build negation zones — any word within 3 tokens after a negation word
    negated_zones = set()
    i = 0
    while i < len(tokens):
        if tokens[i] in NEGATION_WORDS:
            for j in range(i + 1, min(i + 4, len(tokens))):
                negated_zones.add(tokens[j])
        i += 1

    # Lemmatize (keeping negation words, removing other stopwords)
    lemmatized = []
    for token, pos in pos_tags:
        if token in _stop_words:
            continue
        wn_pos = _get_wordnet_pos(pos)
        lemma = _lemmatizer.lemmatize(token, wn_pos)
        lemmatized.append(lemma)

    # Stems for fuzzy fallback
    stems = [_stemmer.stem(t) for t in lemmatized]

    return {
        'tokens': lemmatized,
        'stems': stems,
        'original_lower': original_lower,
        'negated_zones': negated_zones,
    }