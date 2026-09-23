# Lab 3 – Tokenization and Embedding Analysis of Software Datasets

## 1. Objective

The objective of this lab is to apply different tokenization techniques to the software dataset prepared in Lab 2 and analyze their behavior.

Three types of tokenizers were implemented:

* Character-level tokenizer
* Word-level tokenizer
* Subword-level tokenizer using BPE

The tokenizers were compared using:

* Vocabulary size
* Average sequence length
* Embedding matrix size

A subword tokenizer was then selected for further analysis. A random embedding matrix was initialized, the most frequent tokens were identified, and cosine similarity between token embeddings was calculated.

---

## 2. Dataset Used

The dataset used in this lab is the cleaned source-code dataset generated in **Lab 2**:

```text
lab2/data/cleaned_source_code_dataset.csv
```

The dataset contains metadata about source files from five open-source repositories:

| Repository   | Source Files |
| ------------ | -----------: |
| Flask        |          106 |
| Requests     |           39 |
| Pytest       |          276 |
| FastAPI      |         1155 |
| Scikit-learn |         1092 |
| **Total**    |     **2668** |

The CSV dataset was used to identify the source files, while the actual source-code contents were read from the cloned repositories.

During execution, **2620 source files** were successfully loaded from the dataset and used for tokenization.

---

## 3. Repositories

The following repositories were used:

* Flask
* Requests
* Pytest
* FastAPI
* Scikit-learn

---

## 4. Technology Stack

| Technology              | Purpose                                                |
| ----------------------- | ------------------------------------------------------ |
| Python                  | Main programming language                              |
| CSV                     | Reading the Lab 2 source-code dataset                  |
| Regular Expressions     | Implementing the word tokenizer                        |
| Hugging Face Tokenizers | Implementing the BPE subword tokenizer                 |
| NumPy                   | Creating embedding matrices and calculating similarity |
| JSON                    | Storing experiment statistics and results              |
| Git/GitHub              | Version control and project submission                 |

### Association with the Project

Python is used to implement the complete experiment.

The Lab 2 CSV file provides the list of source files. The program uses the repository and file path information to locate and read the actual source-code files.

The Tokenizers library is used to train the BPE subword tokenizer.

NumPy is used to create the random embedding matrix and perform vector calculations such as cosine similarity.

JSON files are generated to store the results so that the experiment results are preserved separately from the terminal output.

---

# 5. Source-Code Loading

The program reads:

```text
lab2/data/cleaned_source_code_dataset.csv
```

For every record, it identifies:

* Repository
* File path

The repository path is then combined with the file path to locate the actual source file.

Files that exist are read and their source code is stored for tokenization.

The experiment successfully loaded:

```text
Total source files loaded: 2620
```

---

# 6. Character-Level Tokenizer

The character tokenizer treats every individual character as a token.

For example:

```text
def add(a, b):
```

is broken into individual characters such as:

```text
d
e
f
a
d
d
(
a
,
...
```

The implementation uses Python's `list()` function on the source-code string.

### Results

| Metric                  |    Result |
| ----------------------- | --------: |
| Vocabulary Size         |       299 |
| Average Sequence Length |   9291.73 |
| Embedding Dimension     |       128 |
| Embedding Matrix        | 299 × 128 |
| Total Matrix Elements   |    38,272 |

### Observation

The character tokenizer has a very small vocabulary because programming source code uses a limited set of characters.

However, each source file produces a long sequence because every character becomes a separate token.

---

# 7. Word-Level Tokenizer

The word tokenizer separates identifiers, numbers and punctuation using a regular expression.

The tokenizer recognizes programming identifiers such as:

```text
def
self
import
pytest
```

while punctuation such as:

```text
(
)
,
=
:
```

is also treated as a token.

### Results

| Metric                  |       Result |
| ----------------------- | -----------: |
| Vocabulary Size         |       67,194 |
| Average Sequence Length |      1910.28 |
| Embedding Dimension     |          128 |
| Embedding Matrix        | 67,194 × 128 |
| Total Matrix Elements   |    8,600,832 |

### Observation

The word tokenizer has a much larger vocabulary because software repositories contain many different identifiers, names and combinations of tokens.

The average sequence length is much smaller than the character tokenizer because multiple characters form a single token.

---

# 8. Subword-Level Tokenizer

A **Byte Pair Encoding (BPE)** tokenizer was selected for the subword experiment.

The tokenizer was trained using the source-code corpus with a target vocabulary size of:

```text
5000
```

Subword tokenization can represent complete words when they are common while splitting less common words or identifiers into smaller pieces.

### Results

| Metric                  |      Result |
| ----------------------- | ----------: |
| Vocabulary Size         |       5,000 |
| Average Sequence Length |     2068.06 |
| Embedding Dimension     |         128 |
| Embedding Matrix        | 5,000 × 128 |
| Total Matrix Elements   |     640,000 |

---

# 9. Tokenizer Comparison

| Tokenizer     | Vocabulary Size | Average Sequence Length | Embedding Matrix |
| ------------- | --------------: | ----------------------: | ---------------: |
| Character     |             299 |                 9291.73 |        299 × 128 |
| Word          |          67,194 |                 1910.28 |     67,194 × 128 |
| Subword (BPE) |           5,000 |                 2068.06 |      5,000 × 128 |

The embedding dimension was kept fixed at **128** for all comparisons.

### Analysis

The character tokenizer has the smallest vocabulary but the longest sequences.

The word tokenizer has the largest vocabulary and a shorter sequence length.

The BPE tokenizer provides a controlled vocabulary of 5,000 tokens while maintaining a sequence length close to the word tokenizer.

The results demonstrate the trade-off between vocabulary size and sequence length.

---

# 10. Embedding Matrix

For the subword tokenizer, a random embedding matrix was initialized.

The embedding dimension was:

```text
128
```

Therefore, the subword embedding matrix has the shape:

```text
5000 × 128
```

and contains:

```text
640,000
```

values.

A fixed random seed was used:

```python
np.random.seed(42)
```

This makes the experiment reproducible, meaning the same random embeddings and similarity results are obtained when the program is executed again.

---

# 11. Top 50 Most Frequent Subword Tokens

The frequency of every subword token was counted using Python's `Counter`.

The most frequent tokens included:

| Token  | Frequency |
| ------ | --------: |
| `.`    |   270,518 |
| `,`    |   212,428 |
| `(`    |   173,698 |
| `=`    |   161,988 |
| `"`    |   114,364 |
| `)`    |    99,952 |
| `:`    |    75,359 |
| `0`    |    54,323 |
| `",`   |    50,903 |
| `1`    |    50,587 |
| `the`  |    49,628 |
| `#`    |    48,799 |
| `-`    |    47,998 |
| `":`   |    47,113 |
| `_`    |    47,105 |
| `[`    |    41,415 |
| `X`    |    32,957 |
| `self` |    31,437 |
| `def`  |    29,452 |
| `of`   |    28,658 |

The complete Top 50 list is stored in:

```text
lab3/output/embedding_analysis.json
```

---

# 12. Top 10 Most Similar Embedding Pairs

Cosine similarity was calculated between pairs of the top 50 tokens.

The highest similarities obtained were:

| Token 1 | Token 2 | Similarity |
| ------- | ------- | ---------: |
| `)`     | `None`  |     0.8251 |
| `to`    | `None`  |     0.8203 |
| `None`  | `for`   |     0.8163 |
| `#`     | `("`    |     0.8120 |
| `a`     | `y`     |     0.8098 |
| `the`   | `s`     |     0.8092 |
| `(`     | `to`    |     0.8090 |
| `self`  | `to`    |     0.8090 |
| `(`     | `=`     |     0.8075 |
| `:`     | `test_` |     0.8073 |

---

# 13. Top 10 Least Similar Embedding Pairs

The lowest similarities among the top 50 tokens were:

| Token 1 | Token 2  | Similarity |
| ------- | -------- | ---------: |
| `],`    | `")`     |     0.6597 |
| `",`    | `is`     |     0.6663 |
| `.`     | `pytest` |     0.6742 |
| `X`     | `]`      |     0.6772 |
| `2`     | `/`      |     0.6845 |
| `(`     | `{`      |     0.6847 |
| `_`     | `np`     |     0.6856 |
| `def`   | `from`   |     0.6860 |
| `-`     | `":`     |     0.6866 |
| `{`     | `],`     |     0.6878 |

### Important Observation

The embeddings used in this experiment were **randomly initialized**.

Therefore, these similarity values should not be interpreted as learned semantic relationships between the tokens.

The similarity experiment demonstrates the mathematical calculation and the later improvement algorithm, rather than showing a trained language model's understanding of programming concepts.

---

# 14. Selected Tokens

Five tokens from the Top 50 were selected for individual analysis:

```text
def
self
import
pytest
None
```

Their most similar tokens according to the random embedding matrix were:

| Selected Token | Most Similar Token | Similarity |
| -------------- | ------------------ | ---------: |
| `def`          | `(`                |     0.7919 |
| `self`         | `to`               |     0.8090 |
| `import`       | `if`               |     0.7967 |
| `pytest`       | `a`                |     0.7974 |
| `None`         | `)`                |     0.8251 |

At least two selected tokens should be different from the tokens selected by the student next to me, as required by the lab instruction.

---

# 15. Similarity Between Selected Related Pairs

For the improvement experiment, three programming-related token pairs were manually selected:

```text
def      ↔ self
pytest   ↔ assert
import   ↔ from
```

Their original cosine similarities were:

| Pair                | Original Similarity |
| ------------------- | ------------------: |
| `def` ↔ `self`      |              0.7225 |
| `pytest` ↔ `assert` |              0.7380 |
| `import` ↔ `from`   |              0.7376 |

These pairs were selected manually for the experiment. Their initial similarity does not indicate that the random embedding model learned that they are related.

---

# 16. Naive Algorithm to Improve Similarity

### Algorithm

1. Select related token pairs manually.
2. Obtain the embedding vector of both tokens.
3. Calculate the midpoint of the two vectors.
4. Move both vectors slightly toward the midpoint.
5. Keep unrelated token embeddings unchanged.
6. Calculate cosine similarity again.
7. Compare the similarity before and after the update.

---

# 17. Similarity After Improvement

After applying the naive algorithm, the similarities increased:

| Pair                | Before |  After |  Change |
| ------------------- | -----: | -----: | ------: |
| `def` ↔ `self`      | 0.7225 | 0.7692 | +0.0467 |
| `pytest` ↔ `assert` | 0.7380 | 0.7824 | +0.0444 |
| `import` ↔ `from`   | 0.7376 | 0.7821 | +0.0445 |

### Observation

All three selected pairs showed an increase in cosine similarity.

This happens because the algorithm moves the two selected vectors toward their midpoint, reducing the difference between the vectors.

However, this is only a **naive demonstration**. It does not train embeddings from real semantic relationships in the source-code dataset.

---

# 18. Output Files

The experiment generates the following JSON files:

```text
lab3/output/
├── character_tokenizer_statistics.json
├── word_tokenizer_statistics.json
├── subword_tokenizer_statistics.json
├── embedding_analysis.json
├── selected_token_similarity.json
├── original_related_token_similarity.json
├── improved_embedding_similarity.json
└── screenshots/
```

# 19. Problems / Applications of the Dataset

The software source-code dataset and tokenization analysis can be used in several software engineering and machine learning applications.

### 1. Code Search

Tokenized source code can be used to build systems that search for functions, identifiers or programming patterns.

### 2. Code Completion

Token sequences can be used as input for models that predict the next token while writing source code.

### 3. Bug Detection

Tokenized source code can be analyzed to identify patterns associated with defects or incorrect programming constructs.

### 4. Code Classification

Repositories or source files can be classified according to programming language, functionality or other software characteristics.

### 5. Code Similarity Analysis

Token representations can be used to compare source files and identify similar code structures.

### 6. Software Repository Mining

Token-level information can be combined with repository-level information to study how source code evolves over time.

---

# 20. Limitations

There are several limitations in this experiment.

### Random Embeddings

The embedding matrix was randomly initialized instead of being trained on the source-code corpus. Therefore, the initial cosine similarities do not represent actual semantic relationships.

### Simple Word Tokenization

The word tokenizer uses a regular expression and does not perform full programming-language parsing.

### Fixed BPE Vocabulary

The BPE tokenizer was trained with a vocabulary size of 5,000. Different vocabulary sizes could produce different sequence lengths and token distributions.


# 21. Learning Outcomes

After completing this lab, the following concepts were practiced:

* Character-level tokenization
* Word-level tokenization
* Subword tokenization
* Byte Pair Encoding (BPE)
* Vocabulary size
* Sequence length
* Embedding dimensions
* Embedding matrix size
* Token frequency analysis
* Cosine similarity
* Random embedding initialization
* Comparing token embeddings
* Designing a simple embedding-update algorithm
* Before/after similarity analysis

# 22. Conclusion

This lab analyzed source code from five open-source repositories using character, word and subword tokenization techniques.

The comparison showed that character tokenization produces a small vocabulary but very long sequences, while word tokenization produces a much larger vocabulary. The BPE tokenizer provided a controlled vocabulary of 5,000 tokens with an average sequence length of 2068.06 tokens.

A random embedding matrix was then created for the BPE vocabulary. The top 50 most frequent tokens were identified and cosine similarities between their embeddings were calculated.

Finally, three manually selected programming-related token pairs were used to demonstrate a simple similarity-improvement algorithm. Moving the selected embeddings toward their midpoint increased the cosine similarity for all three pairs.
