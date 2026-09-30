import json
import os
import random
import numpy as np

from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.trainers import BpeTrainer


# --------------------------------
# Configuration
# --------------------------------

EMBEDDING_DIMENSION = 128
CONTEXT_WINDOW = 2


# --------------------------------
# Paths
# --------------------------------

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
    "lab4",
    "output"
)


# --------------------------------
# Load source files
# --------------------------------

def load_source_files():

    source_files = []

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        lines = file.readlines()

    for line in lines[1:]:

        parts = line.strip().split(",")

        if len(parts) < 6:
            continue

        repository = parts[0]
        file_path = parts[1]

        if repository not in REPOSITORIES:
            continue

        full_path = os.path.join(
            REPOSITORIES[repository],
            file_path
        )

        if os.path.exists(full_path):

            try:

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

            except Exception:
                continue

    print("Source files loaded:", len(source_files))

    return source_files


# --------------------------------
# Create BPE tokenizer
# --------------------------------

def create_tokenizer(source_files):

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
        trainer
    )

    return tokenizer


# --------------------------------
# Get vocabulary
# --------------------------------

def get_vocabulary(tokenizer):

    vocabulary = tokenizer.get_vocab()

    tokens = list(vocabulary.keys())

    return tokens


# --------------------------------
# Select 20 tokens
# --------------------------------

def select_tokens(tokens):

    random.seed(42)

    valid_tokens = [
        token
        for token in tokens
        if token != "[UNK]"
    ]

    # Sort before sampling so selection
    # remains reproducible
    valid_tokens.sort()

    selected_tokens = random.sample(
        valid_tokens,
        20
    )

    print("\nSelected 20 tokens:")

    for token in selected_tokens:
        print(token)

    return selected_tokens


# --------------------------------
# Approach 1
# Random Embeddings
# --------------------------------

def random_embeddings(tokens):

    np.random.seed(42)

    embeddings = np.random.rand(
        len(tokens),
        EMBEDDING_DIMENSION
    )

    return embeddings


# --------------------------------
# Cosine similarity
# --------------------------------

def cosine_similarity(vector_a, vector_b):

    numerator = np.dot(
        vector_a,
        vector_b
    )

    denominator = (
        np.linalg.norm(vector_a)
        *
        np.linalg.norm(vector_b)
    )

    if denominator == 0:
        return 0

    return numerator / denominator


# --------------------------------
# Pairwise similarity
# --------------------------------

def calculate_pairwise_similarity(
    tokens,
    embeddings
):

    similarities = []

    for i in range(len(tokens)):

        for j in range(
            i + 1,
            len(tokens)
        ):

            similarity = cosine_similarity(
                embeddings[i],
                embeddings[j]
            )

            similarities.append({
                "token1": tokens[i],
                "token2": tokens[j],
                "similarity": float(similarity)
            })

    return similarities


# --------------------------------
# Top 5 similar pairs
# --------------------------------

def get_top_similar_pairs(
    similarities
):

    sorted_similarities = sorted(
        similarities,
        key=lambda x: x["similarity"],
        reverse=True
    )

    return sorted_similarities[:5]


# --------------------------------
# Approach 2
# Context-based Embeddings
# --------------------------------

def context_embeddings(
    source_files,
    tokenizer,
    selected_tokens
):

    token_index = {
        token: index
        for index, token in enumerate(
            selected_tokens
        )
    }

    embeddings = np.zeros(
        (
            len(selected_tokens),
            len(selected_tokens)
        )
    )

    for file in source_files:

        tokens = tokenizer.encode(
            file["code"]
        ).tokens

        for i, token in enumerate(tokens):

            if token not in token_index:
                continue

            token_id = token_index[token]

            start = max(
                0,
                i - CONTEXT_WINDOW
            )

            end = min(
                len(tokens),
                i + CONTEXT_WINDOW + 1
            )

            for j in range(start, end):

                if i == j:
                    continue

                context_token = tokens[j]

                if context_token in token_index:

                    context_id = token_index[
                        context_token
                    ]

                    embeddings[
                        token_id,
                        context_id
                    ] += 1

    return embeddings

# --------------------------------
# Save results
# --------------------------------

def save_results(
    selected_tokens,
    random_top_5,
    context_top_5
):

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    results = {
        "selected_tokens": selected_tokens,
        "random_embeddings": {
            "embedding_dimension": EMBEDDING_DIMENSION,
            "top_5_similar_pairs": random_top_5
        },
        "context_embeddings": {
            "context_window": CONTEXT_WINDOW,
            "top_5_similar_pairs": context_top_5
        }
    }

    output_path = os.path.join(
        OUTPUT_DIR,
        "custom_embedding_results.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )

    print(
        "\nResults saved to:",
        output_path
    )

# --------------------------------
# Main
# --------------------------------

def main():

    # Load source code
    source_files = load_source_files()

    # Create tokenizer
    tokenizer = create_tokenizer(
        source_files
    )

    # Get vocabulary
    tokens = get_vocabulary(
        tokenizer
    )

    print(
        "Vocabulary size:",
        len(tokens)
    )

    # Select 20 tokens
    selected_tokens = select_tokens(
        tokens
    )

    # =================================
    # Approach 1: Random Embeddings
    # =================================

    random_matrix = random_embeddings(
        selected_tokens
    )

    random_similarities = (
        calculate_pairwise_similarity(
            selected_tokens,
            random_matrix
        )
    )

    random_top_5 = get_top_similar_pairs(
        random_similarities
    )

    print(
        "\nTop 5 Similar Pairs - "
        "Random Embeddings:"
    )

    for pair in random_top_5:

        print(
            pair["token1"],
            "<->",
            pair["token2"],
            ":",
            round(
                pair["similarity"],
                4
            )
        )

    # =================================
    # Approach 2: Context Embeddings
    # =================================

    context_matrix = context_embeddings(
        source_files,
        tokenizer,
        selected_tokens
    )

    context_similarities = (
        calculate_pairwise_similarity(
            selected_tokens,
            context_matrix
        )
    )

    context_top_5 = get_top_similar_pairs(
        context_similarities
    )

    print(
        "\nTop 5 Similar Pairs - "
        "Context Embeddings:"
    )

    for pair in context_top_5:

        print(
            pair["token1"],
            "<->",
            pair["token2"],
            ":",
            round(
                pair["similarity"],
                4
            )
        )
     # Save results
    save_results(
        selected_tokens,
        random_top_5,
        context_top_5
    )

# --------------------------------
# Program entry point
# --------------------------------

if __name__ == "__main__":
    main()