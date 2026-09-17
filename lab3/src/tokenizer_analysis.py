import os
import csv
import re
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

# CSET456Lab folder
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

# Location of the five repositories
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

            # Remove repository name from the beginning of the path
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


def character_tokenizer(source_files):
    all_tokens = []
    sequence_lengths = []

    for file in source_files:
        tokens = list(file["code"])

        all_tokens.extend(tokens)
        sequence_lengths.append(len(tokens))

    vocab_size = len(set(all_tokens))
    average_sequence_length = sum(sequence_lengths) / len(sequence_lengths)

    return vocab_size, average_sequence_length


def word_tokenizer(source_files):
    all_tokens = []
    sequence_lengths = []

    for file in source_files:
        code = file["code"]

        # Separate words, identifiers and symbols
        tokens = re.findall(
            r"[A-Za-z_][A-Za-z0-9_]*|[^\sA-Za-z0-9_]",
            code
        )

        all_tokens.extend(tokens)
        sequence_lengths.append(len(tokens))

    vocab_size = len(set(all_tokens))
    average_sequence_length = sum(sequence_lengths) / len(sequence_lengths)

    return vocab_size, average_sequence_length

def subword_tokenizer(source_files):
    tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
    tokenizer.pre_tokenizer = Whitespace()

    trainer = BpeTrainer(
        vocab_size=5000,
        special_tokens=["[UNK]"]
    )

    corpus = [file["code"] for file in source_files]

    tokenizer.train_from_iterator(corpus, trainer=trainer)

    all_tokens = []
    sequence_lengths = []

    for code in corpus:
        tokens = tokenizer.encode(code).tokens

        all_tokens.extend(tokens)
        sequence_lengths.append(len(tokens))

    vocab_size = tokenizer.get_vocab_size()
    average_sequence_length = sum(sequence_lengths) / len(sequence_lengths)

    return tokenizer, all_tokens, vocab_size, average_sequence_length


def embedding_matrix_size(vocab_size):
    return vocab_size * EMBEDDING_DIMENSION


def main():
    source_files = load_source_files()

    print("Total source files loaded:", len(source_files))

    # Character tokenizer
    char_vocab, char_avg_length = character_tokenizer(source_files)
    char_embedding = embedding_matrix_size(char_vocab)

    # Word tokenizer
    word_vocab, word_avg_length = word_tokenizer(source_files)
    word_embedding = embedding_matrix_size(word_vocab)

    # Subword tokenizer
    subword_tokenizer_obj, subword_tokens, subword_vocab, subword_avg_length = subword_tokenizer(source_files)
    subword_embedding = embedding_matrix_size(subword_vocab)

    # Character results
    print("\nCharacter Tokenizer")
    print("-------------------")
    print("Vocabulary size:", char_vocab)
    print("Average sequence length:", round(char_avg_length, 2))
    print(
        "Embedding matrix size:",
        char_vocab,
        "x",
        EMBEDDING_DIMENSION,
        "=",
        char_embedding
    )

    # Word results
    print("\nWord Tokenizer")
    print("----------------")
    print("Vocabulary size:", word_vocab)
    print("Average sequence length:", round(word_avg_length, 2))
    print(
        "Embedding matrix size:",
        word_vocab,
        "x",
        EMBEDDING_DIMENSION,
        "=",
        word_embedding
    )

    # Subword results
    print("\nSubword Tokenizer (BPE)")
    print("-----------------------")
    print("Vocabulary size:", subword_vocab)
    print("Average sequence length:", round(subword_avg_length, 2))
    print(
        "Embedding matrix size:",
        subword_vocab,
        "x",
        EMBEDDING_DIMENSION,
        "=",
        subword_embedding
    )

    # Comparison
    print("\nTokenizer Comparison")
    print("--------------------")
    print("Tokenizer\tVocabulary\tAverage Sequence\tEmbedding Matrix")

    print(
        "Character\t",
        char_vocab,
        "\t\t",
        round(char_avg_length, 2),
        "\t\t",
        char_embedding
    )

    print(
        "Word\t\t",
        word_vocab,
        "\t\t",
        round(word_avg_length, 2),
        "\t\t",
        word_embedding
    )

    print(
        "Subword\t\t",
        subword_vocab,
        "\t\t",
        round(subword_avg_length, 2),
        "\t\t",
        subword_embedding
    )


if __name__ == "__main__":
    main()