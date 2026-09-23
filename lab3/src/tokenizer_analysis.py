import os
import csv
import re
import json
from collections import Counter

import numpy as np

from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

REPOSITORIES = {
    "flask": os.path.join(BASE_DIR, "..", "flask"),
    "requests": os.path.join(BASE_DIR, "..", "requests"),
    "pytest": os.path.join(BASE_DIR, "..", "pytest"),
    "fastapi": os.path.join(BASE_DIR, "..", "fastapi"),
    "scikit-learn": os.path.join(BASE_DIR, "..", "scikit-learn")
}

DATASET_PATH = os.path.join(
    BASE_DIR,
    "lab2",
    "data",
    "cleaned_source_code_dataset.csv"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "lab3",
    "output"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

EMBEDDING_DIMENSION = 128

# Fixed seed so the random experiment gives the same
# results every time the program is executed.
np.random.seed(42)


# ---------------------------------------------------------
# LOAD SOURCE CODE
# ---------------------------------------------------------

def load_source_files():

    source_files = []

    with open(DATASET_PATH, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            repository = row["repository"]
            file_path = row["file_path"]

            if repository not in REPOSITORIES:
                continue

            repo_path = REPOSITORIES[repository]

            prefix = repository + "\\"

            if file_path.startswith(prefix):
                file_path = file_path[len(prefix):]

            full_path = os.path.join(repo_path, file_path)

            if os.path.exists(full_path):

                with open(
                    full_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as source:

                    code = source.read()

                source_files.append({
                    "repository": repository,
                    "file_path": file_path,
                    "code": code
                })

    return source_files


# ---------------------------------------------------------
# CHARACTER TOKENIZER
# ---------------------------------------------------------

def character_tokenizer(source_files):

    all_tokens = []
    sequence_lengths = []

    for file in source_files:

        tokens = list(file["code"])

        all_tokens.extend(tokens)
        sequence_lengths.append(len(tokens))

    vocab_size = len(set(all_tokens))

    average_sequence_length = (
        sum(sequence_lengths) / len(sequence_lengths)
    )

    return vocab_size, average_sequence_length


# ---------------------------------------------------------
# WORD TOKENIZER
# ---------------------------------------------------------

def word_tokenizer(source_files):

    all_tokens = []
    sequence_lengths = []

    for file in source_files:

        code = file["code"]

        tokens = re.findall(
            r"[A-Za-z_][A-Za-z0-9_]*|[^\sA-Za-z0-9_]",
            code
        )

        all_tokens.extend(tokens)
        sequence_lengths.append(len(tokens))

    vocab_size = len(set(all_tokens))

    average_sequence_length = (
        sum(sequence_lengths) / len(sequence_lengths)
    )

    return vocab_size, average_sequence_length


# ---------------------------------------------------------
# SUBWORD TOKENIZER - BPE
# ---------------------------------------------------------

def subword_tokenizer(source_files):

    tokenizer = Tokenizer(
        BPE(unk_token="[UNK]")
    )

    tokenizer.pre_tokenizer = Whitespace()

    trainer = BpeTrainer(
        vocab_size=5000,
        special_tokens=["[UNK]"]
    )

    corpus = [
        file["code"]
        for file in source_files
    ]

    tokenizer.train_from_iterator(
        corpus,
        trainer=trainer
    )

    all_tokens = []
    sequence_lengths = []

    for code in corpus:

        tokens = tokenizer.encode(code).tokens

        all_tokens.extend(tokens)
        sequence_lengths.append(len(tokens))

    vocab_size = tokenizer.get_vocab_size()

    average_sequence_length = (
        sum(sequence_lengths) / len(sequence_lengths)
    )

    return (
        tokenizer,
        all_tokens,
        vocab_size,
        average_sequence_length
    )


# ---------------------------------------------------------
# EMBEDDING MATRIX SIZE
# ---------------------------------------------------------

def embedding_matrix_size(vocab_size):

    return vocab_size * EMBEDDING_DIMENSION


# ---------------------------------------------------------
# SAVE JSON
# ---------------------------------------------------------

def save_json(filename, data):

    path = os.path.join(
        OUTPUT_DIR,
        filename
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )

    print("Saved:", path)


# ---------------------------------------------------------
# TASK 2
# TOP 50 + RANDOM EMBEDDINGS
# ---------------------------------------------------------

def analyze_embeddings(tokenizer, subword_tokens):

    token_counts = Counter(subword_tokens)

    top_50 = token_counts.most_common(50)

    vocabulary = tokenizer.get_vocab()

    vocab_size = tokenizer.get_vocab_size()

    # Random embedding matrix
    embedding_matrix = np.random.rand(
        vocab_size,
        EMBEDDING_DIMENSION
    )

    pairs = []

    # Compare every pair of Top 50 tokens
    for i in range(len(top_50)):

        token1 = top_50[i][0]

        id1 = vocabulary[token1]

        vector1 = embedding_matrix[id1]

        for j in range(i + 1, len(top_50)):

            token2 = top_50[j][0]

            id2 = vocabulary[token2]

            vector2 = embedding_matrix[id2]

            similarity = np.dot(
                vector1,
                vector2
            ) / (
                np.linalg.norm(vector1)
                *
                np.linalg.norm(vector2)
            )

            pairs.append(
                (
                    token1,
                    token2,
                    float(similarity)
                )
            )

    most_similar = sorted(
        pairs,
        key=lambda x: x[2],
        reverse=True
    )[:10]

    least_similar = sorted(
        pairs,
        key=lambda x: x[2]
    )[:10]

    return (
        top_50,
        most_similar,
        least_similar,
        embedding_matrix
    )


# ---------------------------------------------------------
# TASK 3
# SELECT 5 TOKENS
# ---------------------------------------------------------

def find_most_similar_tokens(
    tokenizer,
    top_50,
    embedding_matrix
):

    vocabulary = tokenizer.get_vocab()

    # Five selected tokens from Top 50.
    selected_tokens = [
        "def",
        "self",
        "import",
        "pytest",
        "None"
    ]

    results = []

    for selected_token in selected_tokens:

        token_id = vocabulary[selected_token]

        selected_vector = embedding_matrix[token_id]

        similarities = []

        for token, count in top_50:

            if token == selected_token:
                continue

            other_id = vocabulary[token]

            other_vector = embedding_matrix[other_id]

            similarity = np.dot(
                selected_vector,
                other_vector
            ) / (
                np.linalg.norm(selected_vector)
                *
                np.linalg.norm(other_vector)
            )

            similarities.append(
                (
                    token,
                    float(similarity)
                )
            )

        similarities.sort(
            key=lambda x: x[1],
            reverse=True
        )

        most_similar_token = similarities[0]

        results.append({
            "selected_token": selected_token,
            "most_similar_token": most_similar_token[0],
            "similarity": most_similar_token[1]
        })

    return results


# ---------------------------------------------------------
# TASK 5
# NAIVE ALGORITHM
# ---------------------------------------------------------

def improve_related_embeddings(
    tokenizer,
    embedding_matrix,
    related_pairs,
    learning_rate=0.1
):

    vocabulary = tokenizer.get_vocab()

    updated_matrix = embedding_matrix.copy()

    for token1, token2 in related_pairs:

        id1 = vocabulary[token1]
        id2 = vocabulary[token2]

        vector1 = updated_matrix[id1]
        vector2 = updated_matrix[id2]

        # Calculate midpoint
        midpoint = (vector1 + vector2) / 2

        # Move both vectors slightly toward midpoint
        updated_matrix[id1] = (
            vector1
            + learning_rate * (midpoint - vector1)
        )

        updated_matrix[id2] = (
            vector2
            + learning_rate * (midpoint - vector2)
        )

    return updated_matrix


# ---------------------------------------------------------
# CALCULATE SIMILARITY BETWEEN PAIRS
# ---------------------------------------------------------

def check_pair_similarities(
    tokenizer,
    embedding_matrix,
    pairs
):

    vocabulary = tokenizer.get_vocab()

    results = []

    for token1, token2 in pairs:

        id1 = vocabulary[token1]
        id2 = vocabulary[token2]

        vector1 = embedding_matrix[id1]
        vector2 = embedding_matrix[id2]

        similarity = np.dot(
            vector1,
            vector2
        ) / (
            np.linalg.norm(vector1)
            *
            np.linalg.norm(vector2)
        )

        results.append({
            "token1": token1,
            "token2": token2,
            "similarity": float(similarity)
        })

    return results


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    # -----------------------------------------------------
    # LOAD DATA
    # -----------------------------------------------------

    source_files = load_source_files()

    print(
        "Total source files loaded:",
        len(source_files)
    )


    # -----------------------------------------------------
    # TASK 1 - TOKENIZERS
    # -----------------------------------------------------

    character_vocab, character_avg = character_tokenizer(
        source_files
    )

    character_embedding = embedding_matrix_size(
        character_vocab
    )


    word_vocab, word_avg = word_tokenizer(
        source_files
    )

    word_embedding = embedding_matrix_size(
        word_vocab
    )


    (
        subword_tokenizer_obj,
        subword_tokens,
        subword_vocab,
        subword_avg
    ) = subword_tokenizer(source_files)

    subword_embedding = embedding_matrix_size(
        subword_vocab
    )


    # -----------------------------------------------------
    # PRINT TASK 1
    # -----------------------------------------------------

    print("\nCharacter Tokenizer")
    print("-------------------")
    print("Vocabulary size:", character_vocab)
    print(
        "Average sequence length:",
        round(character_avg, 2)
    )
    print(
        "Embedding matrix size:",
        character_vocab,
        "x",
        EMBEDDING_DIMENSION,
        "=",
        character_embedding
    )


    print("\nWord Tokenizer")
    print("----------------")
    print("Vocabulary size:", word_vocab)
    print(
        "Average sequence length:",
        round(word_avg, 2)
    )
    print(
        "Embedding matrix size:",
        word_vocab,
        "x",
        EMBEDDING_DIMENSION,
        "=",
        word_embedding
    )


    print("\nSubword Tokenizer (BPE)")
    print("-----------------------")
    print("Vocabulary size:", subword_vocab)
    print(
        "Average sequence length:",
        round(subword_avg, 2)
    )
    print(
        "Embedding matrix size:",
        subword_vocab,
        "x",
        EMBEDDING_DIMENSION,
        "=",
        subword_embedding
    )


    # -----------------------------------------------------
    # SAVE THREE STATISTICS FILES
    # -----------------------------------------------------

    save_json(
        "character_tokenizer_statistics.json",
        {
            "tokenizer": "Character",
            "vocabulary_size": character_vocab,
            "average_sequence_length": round(
                character_avg,
                2
            ),
            "embedding_dimension": EMBEDDING_DIMENSION,
            "embedding_matrix": (
                f"{character_vocab} x "
                f"{EMBEDDING_DIMENSION}"
            ),
            "embedding_matrix_size": character_embedding
        }
    )


    save_json(
        "word_tokenizer_statistics.json",
        {
            "tokenizer": "Word",
            "vocabulary_size": word_vocab,
            "average_sequence_length": round(
                word_avg,
                2
            ),
            "embedding_dimension": EMBEDDING_DIMENSION,
            "embedding_matrix": (
                f"{word_vocab} x "
                f"{EMBEDDING_DIMENSION}"
            ),
            "embedding_matrix_size": word_embedding
        }
    )


    save_json(
        "subword_tokenizer_statistics.json",
        {
            "tokenizer": "Subword (BPE)",
            "vocabulary_size": subword_vocab,
            "average_sequence_length": round(
                subword_avg,
                2
            ),
            "embedding_dimension": EMBEDDING_DIMENSION,
            "embedding_matrix": (
                f"{subword_vocab} x "
                f"{EMBEDDING_DIMENSION}"
            ),
            "embedding_matrix_size": subword_embedding
        }
    )


    # -----------------------------------------------------
    # TASK 2
    # -----------------------------------------------------

    (
        top_50,
        most_similar,
        least_similar,
        embedding_matrix
    ) = analyze_embeddings(
        subword_tokenizer_obj,
        subword_tokens
    )


    print("\n\nTop 50 Most Frequent Subword Tokens")
    print("-----------------------------------")

    for token, count in top_50:

        print(
            repr(token),
            ":",
            count
        )


    print("\n\nTop 10 Most Similar Embedding Pairs")
    print("-----------------------------------")

    for token1, token2, similarity in most_similar:

        print(
            repr(token1),
            "<->",
            repr(token2),
            ":",
            round(similarity, 4)
        )


    print("\n\nTop 10 Least Similar Embedding Pairs")
    print("------------------------------------")

    for token1, token2, similarity in least_similar:

        print(
            repr(token1),
            "<->",
            repr(token2),
            ":",
            round(similarity, 4)
        )


    # Save Task 2 results
    save_json(
        "embedding_analysis.json",
        {
            "embedding_dimension": EMBEDDING_DIMENSION,
            "embedding_matrix_shape": [
                subword_vocab,
                EMBEDDING_DIMENSION
            ],
            "top_50_tokens": [
                {
                    "token": token,
                    "frequency": count
                }
                for token, count in top_50
            ],
            "top_10_most_similar": [
                {
                    "token1": token1,
                    "token2": token2,
                    "similarity": round(
                        similarity,
                        4
                    )
                }
                for token1, token2, similarity
                in most_similar
            ],
            "top_10_least_similar": [
                {
                    "token1": token1,
                    "token2": token2,
                    "similarity": round(
                        similarity,
                        4
                    )
                }
                for token1, token2, similarity
                in least_similar
            ]
        }
    )


    # -----------------------------------------------------
    # TASK 3
    # -----------------------------------------------------

    selected_results = find_most_similar_tokens(
        subword_tokenizer_obj,
        top_50,
        embedding_matrix
    )


    print(
        "\n\nTask 3 - Selected Tokens and Most Similar Tokens"
    )

    print(
        "------------------------------------------------"
    )

    for result in selected_results:

        print(
            repr(result["selected_token"]),
            "->",
            repr(result["most_similar_token"]),
            ":",
            round(
                result["similarity"],
                4
            )
        )


    save_json(
        "selected_token_similarity.json",
        {
            "selected_tokens": selected_results
        }
    )


    # -----------------------------------------------------
    # TASK 4
    # -----------------------------------------------------

    # These are related programming tokens selected
    # manually for the improvement experiment.
    related_pairs = [
        ("def", "self"),
        ("pytest", "assert"),
        ("import", "from")
    ]


    original_similarities = check_pair_similarities(
        subword_tokenizer_obj,
        embedding_matrix,
        related_pairs
    )


    print("\n\nTask 4 - Similarity Check")
    print("------------------------")

    for result in original_similarities:

        print(
            result["token1"],
            "<->",
            result["token2"],
            ":",
            round(
                result["similarity"],
                4
            )
        )


    save_json(
        "original_related_token_similarity.json",
        {
            "related_pairs": original_similarities
        }
    )


    # -----------------------------------------------------
    # TASK 5
    # NAIVE IMPROVEMENT
    # -----------------------------------------------------

    print("\n\nTask 5 - Improving Related Token Similarity")
    print("-------------------------------------------")

    print("Related token pairs:")

    for token1, token2 in related_pairs:

        print(
            token1,
            "<->",
            token2
        )


    improved_embedding_matrix = improve_related_embeddings(
        subword_tokenizer_obj,
        embedding_matrix,
        related_pairs,
        learning_rate=0.1
    )


    # -----------------------------------------------------
    # TASK 6
    # REPEAT EXPERIMENT
    # -----------------------------------------------------

    improved_similarities = check_pair_similarities(
        subword_tokenizer_obj,
        improved_embedding_matrix,
        related_pairs
    )


    print("\n\nTask 6 - Similarity After Improvement")
    print("-------------------------------------")

    for result in improved_similarities:

        print(
            result["token1"],
            "<->",
            result["token2"],
            ":",
            round(
                result["similarity"],
                4
            )
        )


    # -----------------------------------------------------
    # BEFORE / AFTER COMPARISON
    # -----------------------------------------------------

    comparison = []

    for original, improved in zip(
        original_similarities,
        improved_similarities
    ):

        change = (
            improved["similarity"]
            - original["similarity"]
        )

        comparison.append({
            "token1": original["token1"],
            "token2": original["token2"],
            "before_similarity": round(
                original["similarity"],
                4
            ),
            "after_similarity": round(
                improved["similarity"],
                4
            ),
            "change": round(
                change,
                4
            )
        })


    print("\n\nBefore vs After")
    print("---------------")

    for result in comparison:

        print(
            result["token1"],
            "<->",
            result["token2"],
            "| Before:",
            result["before_similarity"],
            "| After:",
            result["after_similarity"],
            "| Change:",
            result["change"]
        )


    save_json(
        "improved_embedding_similarity.json",
        {
            "algorithm": (
                "Move related token embeddings "
                "slightly toward their midpoint"
            ),
            "learning_rate": 0.1,
            "related_pairs": related_pairs,
            "comparison": comparison
        }
    )


# ---------------------------------------------------------
# PROGRAM START
# ---------------------------------------------------------

if __name__ == "__main__":
    main()