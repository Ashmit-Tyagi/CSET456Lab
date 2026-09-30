# Lab 4 - Code and Token Embeddings

## 1. Objective

The objective of this lab is to experiment with different embedding techniques for software source code.
The lab uses the source-code dataset prepared in Lab 2 and the BPE tokenizer developed and analyzed in Lab 3.

Four embedding approaches were studied:

1. Random Embedding
2. Context/Frequency Embedding
3. Word2Vec
4. Simplified Code2Vec-style AST Embedding

## 2. Dataset Used

The dataset used in this lab is:

`lab2/data/cleaned_source_code_dataset.csv`

The dataset contains source-code file information for five repositories:

* Flask
* Requests
* Pytest
* FastAPI
* Scikit-learn

A total of 2668 source files were available from the dataset and the corresponding cloned repositories.

## 3. Tokenization

The BPE subword tokenizer from Lab 3 was reused in this lab.

The tokenizer was trained with:

* Vocabulary size: 5000
* Tokenization level: Subword/BPE
* Special token: `[UNK]`

The vocabulary was sorted before random selection so that the experiment could be reproduced.

# 4. Embedding Approach 1 - Random Embedding

## Idea

The first approach was created as a baseline.
Each selected token was assigned a random vector of 128 dimensions.
No information about the meaning, context, frequency, or structure of the token was used.
The vectors were generated using NumPy with random seed 42.

## Process

The purpose of this approach was to understand what happens when embeddings contain no learned information.
If two unrelated tokens receive a high cosine similarity, it demonstrates that numerical similarity alone does not guarantee semantic similarity.

## Result

One of the highest similarities was:

`:", <-> ve_ = 0.8106`

This result is expected because the vectors were generated randomly.

## Limitation

Random embeddings do not learn relationships between tokens.
Therefore, a high similarity value can occur between unrelated tokens.

# 5. Embedding Approach 2 - Context/Frequency Embedding

## Idea

The second approach was designed using local token context.
For every selected token, a context window of two tokens on each side was considered.
A 20 x 20 matrix was created because 20 tokens were selected.
Each matrix value represents how often one selected token appeared near another selected token.
Therefore, tokens occurring in similar local contexts can receive similar representations.

## Process

The main idea was based on the distributional assumption:

> Tokens that occur in similar contexts may have similar representations.

Instead of assigning completely random vectors, this approach uses information from the source code itself.

## Result

Some of the highest similarities were:

* `nu <-> ve_ = 0.9675`
* `23 <-> 70 = 0.9130`
* `contour <-> 70 = 0.8000`

## Limitation

Only the selected 20 tokens were used as dimensions of the context representation.
This makes the representation very small and can cause unrelated tokens to have similar context vectors.
It also does not understand the deeper meaning or syntax of the code.


# 6. Exercise 1 - Twenty Selected Tokens

The following 20 tokens were selected randomly and reproducibly using seed 42:

```text
Sequ
23
doctest
contour
ces
_compat
Python
type
Message
ć
nu
:",
70
Number
caplog
cmap
similar
└
32
ve_
```

Pairwise cosine similarity was calculated for every pair of selected tokens.

The five highest-similarity pairs were reported for each embedding approach.


# 7. Representation Failures

At least two representation failures were observed.

## Failure 1 - Random Embedding

The random approach produced:

`:", <-> ve_ = 0.8106`

The similarity is relatively high even though the tokens do not have an obvious semantic relationship.
This shows that random vectors cannot represent meaningful token relationships.

## Failure 2 - Code2Vec-style Embedding

The simplified AST-based representation produced:

`ces <-> type = 1.0000`

Other pairs also had similarities extremely close to 1.0.

This indicates that several different tokens received very similar structural representations.

## Additional Failure - Context Embedding

The context approach produced:

`nu <-> ve_ = 0.9675`

The two tokens do not have an obvious semantic relationship.


# 8. Word2Vec

## Implementation

Word2Vec was implemented using the Gensim library.
The BPE-tokenized source files were treated as sentences.

The following configuration was used:

* Vector size: 128
* Context window: 2
* Minimum count: 1
* Workers: 1
* Random seed: 42
* Epochs: 5

The model learns token representations from surrounding tokens.

Unlike the random embedding approach, Word2Vec updates the vectors during training based on the context in which tokens occur.

## Word2Vec Results

The five highest similarities among the selected tokens were:

1. `23 <-> 70 = 0.8486`
2. `contour <-> cmap = 0.5193`
3. `23 <-> 32 = 0.5095`
4. `70 <-> 32 = 0.4985`
5. `23 <-> nu = 0.4892`

## Observations

Word2Vec produces learned embeddings instead of random vectors.

The similarity values are generally more informative because the model learns from surrounding source-code tokens.

However, some similarities still do not have an obvious semantic interpretation.

For example:

`23 <-> 70 = 0.8486`

These appear to be numerical/subword tokens rather than clearly related programming concepts.
This can happen because Word2Vec learns statistical relationships from the training corpus. Frequent tokens or tokens appearing in similar contexts can become close in the embedding space.


# 9. Comparison of Custom Embeddings and Word2Vec

| Feature                      | Random       | Context/Frequency            | Word2Vec                 |
| ---------------------------- | ------------ | ---------------------------- | ------------------------ |
| Uses source-code information | No           | Yes                          | Yes                      |
| Learns embeddings            | No           | No                           | Yes                      |
| Uses local context           | No           | Yes                          | Yes                      |
| Embedding dimension          | 128          | 20                           | 128                      |
| Captures token relationships | Very limited | Partially                    | Better                   |
| Main limitation              | Randomness   | Small context representation | Depends on training data |

The Random Embedding approach was useful as a baseline because it demonstrated that cosine similarity can be high even without meaningful information.

The Context Embedding approach improved the representation by using local co-occurrence information.

Word2Vec goes further by learning dense 128-dimensional representations from token context.

Therefore, the main conceptual difference is that the first approach assigns vectors without learning, the second explicitly counts local relationships, and Word2Vec learns dense vectors from those relationships during training.


# 10. Simplified Code2Vec-style Embedding

A simplified Code2Vec-style approach was implemented using Python's built-in `ast` module.

The source code was parsed into Abstract Syntax Trees.

AST node types such as:

* FunctionDef
* ClassDef
* Call
* Name
* Assign
* Return
* If
* For

were used to construct structural representations.

The representation was then converted into numeric vectors and cosine similarity was calculated.


# 11. Code2Vec-style Results

The five highest similarities were:

1. `ces <-> type = 1.0000`
2. `32 <-> ve_ = 0.9999`
3. `23 <-> 70 = 0.9998`
4. `70 <-> 32 = 0.9998`
5. `nu <-> ve_ = 0.9998`

The very high similarity values demonstrate a limitation of the simplified implementation.

Many tokens occur in source files having similar AST structures. Therefore, their structural vectors can become almost identical.

This means that the implementation captures code structure at a basic level but does not provide enough token-specific information.


# 12. Overall Observations

The experiment demonstrates that different embedding approaches represent source-code tokens differently.

### Random Embedding

Useful as a baseline, but it does not represent meaningful relationships.

### Context Embedding

Uses actual token co-occurrence and therefore contains information from the source code. However, the representation is limited because only 20 selected tokens are used.

### Word2Vec

Learns dense representations from surrounding tokens and provides a more learned representation of token relationships.

### Code2Vec-style Embedding

Uses source-code structure through AST information. The simplified implementation shows the usefulness of structural information but also demonstrates that a simple AST-frequency representation is not enough to reproduce the capabilities of a full code embedding model.


# 13. Output Files

The final embedding results are stored in:

`lab4/output/embedding_results.json`

The file contains:

* Selected 20 tokens
* Random embedding top-5 pairs
* Context embedding top-5 pairs
* Word2Vec top-5 pairs
* Code2Vec-style top-5 pairs

An earlier intermediate result file is also present:

`lab4/output/custom_embedding_results.json`


# 14. Applications

Embedding techniques can be useful in software engineering problems such as:

* Code search
* Code similarity detection
* Duplicate code detection
* Bug prediction
* Code recommendation
* Program classification
* API recommendation
* Software repository analysis
* Source-code clustering
* Finding related functions or tokens


# 15. Limitations

This experiment has several limitations:

1. Only 20 tokens were selected for the pairwise analysis.
2. The Random Embedding approach does not learn from data.
3. The Context Embedding approach uses a small 20-dimensional co-occurrence representation.
4. Word2Vec performance depends on the training corpus and hyperparameters.
5. BPE tokens are subwords and may not always represent complete programming concepts.
6. The Code2Vec implementation is simplified and should not be considered the original Code2Vec architecture.
7. High cosine similarity does not always imply semantic similarity.


# 16. Learning Outcomes

Through this lab, I learned:

* How embeddings represent tokens as numerical vectors.
* How cosine similarity can compare embedding vectors.
* How random vectors can act as a baseline.
* How local context can be used to construct embeddings.
* How Word2Vec learns representations from token context.
* How ASTs can provide structural information about source code.
* How different embedding methods can produce different similarity results.
* Why a high similarity score does not always mean that two tokens are semantically related.
* The importance of analyzing representation failures rather than looking only at similarity scores.


# 17. Conclusion

This lab compared four different approaches for representing source-code tokens.

The experiments showed that embedding design strongly affects the similarity results. Random embeddings provide a simple baseline, context embeddings use local co-occurrence information, Word2Vec learns dense representations from context, and the simplified Code2Vec-style approach uses structural information from the AST.
The experiment also demonstrated that every representation has limitations. Therefore, cosine similarity should be interpreted together with the way the embeddings were generated and the characteristics of the source-code dataset.
