import os
import re
import json
import random
import numpy as np

from collections import Counter
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.trainers import BpeTrainer

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

def load_source_files():
    source_files = []

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        lines = file.readlines()

    header = lines[0].strip().split(",")

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

def get_vocabulary(tokenizer):
    vocabulary = tokenizer.get_vocab()

    tokens = list(vocabulary.keys())

    return tokens

def select_tokens(tokens):
    random.seed(42)

    valid_tokens = [
        token
        for token in tokens
        if token not in ["[UNK]"]
    ]

    selected_tokens = random.sample(
        valid_tokens,
        20
    )

    print("\nSelected 20 tokens:")

    for token in selected_tokens:
        print(token)

    return selected_tokens

def main():
    source_files = load_source_files()

    tokenizer = create_tokenizer(source_files)

    tokens = get_vocabulary(tokenizer)

    print("Vocabulary size:", len(tokens))

    selected_tokens = select_tokens(tokens)


if __name__ == "__main__":
    main()