import os
import csv
import re
from collections import Counter

import numpy as np

from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace


# CSET456Lab folder
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)


# Repository locations
REPOSITORIES = {
    "flask": os.path.join(BASE_DIR, "..", "flask"),
    "requests": os.path.join(BASE_DIR, "..", "requests"),
    "pytest": os.path.join(BASE_DIR, "..", "pytest"),
    "fastapi": os.path.join(BASE_DIR, "..", "fastapi"),
    "scikit-learn": os.path.join(BASE_DIR, "..", "scikit-learn")
}


# Lab 2 cleaned source-code dataset
DATASET_PATH = os.path.join(
    BASE_DIR,
    "lab2",
    "data",
    "cleaned_source_code_dataset.csv"
)


# Embedding dimension
EMBEDDING_DIMENSION = 128


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

            # Remove repository name from beginning of path
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
# TOP 50 MOST FREQUENT TOKENS
# ---------------------------------------------------------

def get_top_50_tokens(subword_tokens):

    token_counts = Counter(subword_tokens)

    top_50 = token_counts.most_common(50)

    return top_50


# ---------------------------------------------------------
# EMBEDDING ANALYSIS
# ---------------------------------------------------------

def analyze_embeddings(tokenizer, subword_tokens):

    # Count token frequency
    token_counts = Counter(subword_tokens)

    # Get top 50 tokens
    top_50 = token_counts.most_common(50)

    # Get tokenizer vocabulary
    vocabulary = tokenizer.get_vocab()

    # Create random embedding matrix
    vocab_size = tokenizer.get_vocab_size()

    embedding_matrix = np.random.rand(
        vocab_size,
        EMBEDDING_DIMENSION
    )

    pairs = []

    # Compare every pair among the top 50 tokens
    for i in range(len(top_50)):

        token1 = top_50[i][0]

        id1 = vocabulary[token1]

        vector1 = embedding_matrix[id1]

        for j in range(i + 1, len(top_50)):

            token2 = top_50[j][0]

            id2 = vocabulary[token2]

            vector2 = embedding_matrix[id2]

            # Cosine similarity
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
                    similarity
                )
            )

    # Highest similarities
    most_similar = sorted(
        pairs,
        key=lambda x: x[2],
        reverse=True
    )[:10]

    # Lowest similarities
    least_similar = sorted(
        pairs,
        key=lambda x: x[2]
    )[:10]

    return (
        top_50,
        most_similar,
        least_similar
    )


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    # Load source files
    source_files = load_source_files()

    print(
        "Total source files loaded:",
        len(source_files)
    )


    # -----------------------------------------------------
    # TASK 1
    # -----------------------------------------------------

    # Character tokenizer
    character_vocab, character_avg = character_tokenizer(
        source_files
    )

    character_embedding = embedding_matrix_size(
        character_vocab
    )


    # Word tokenizer
    word_vocab, word_avg = word_tokenizer(
        source_files
    )

    word_embedding = embedding_matrix_size(
        word_vocab
    )


    # Subword tokenizer
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
    # TASK 1 OUTPUT
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


    print("\nTokenizer Comparison")
    print("--------------------")

    print(
        "Tokenizer       Vocabulary      "
        "Average Sequence        Embedding Matrix"
    )

    print(
        "Character        ",
        character_vocab,
        "           ",
        round(character_avg, 2),
        "                 ",
        character_embedding
    )

    print(
        "Word             ",
        word_vocab,
        "         ",
        round(word_avg, 2),
        "                 ",
        word_embedding
    )

    print(
        "Subword          ",
        subword_vocab,
        "           ",
        round(subword_avg, 2),
        "                 ",
        subword_embedding
    )


    # -----------------------------------------------------
    # TASK 2
    # -----------------------------------------------------

    (
        top_50,
        most_similar,
        least_similar
    ) = analyze_embeddings(
        subword_tokenizer_obj,
        subword_tokens
    )


    # -----------------------------------------------------
    # TOP 50 TOKENS
    # -----------------------------------------------------

    print("\n\nTop 50 Most Frequent Subword Tokens")
    print("-----------------------------------")

    for token, count in top_50:

        print(
            repr(token),
            ":",
            count
        )


    # -----------------------------------------------------
    # MOST SIMILAR
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # LEAST SIMILAR
    # -----------------------------------------------------

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


# ---------------------------------------------------------
# PROGRAM START
# ---------------------------------------------------------

if __name__ == "__main__":
    main()