import os
import csv

# CSET456Lab folder
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

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
                with open(full_path, "r", encoding="utf-8", errors="ignore") as source:
                    code = source.read()

                source_files.append({
                    "repository": repository,
                    "file_path": file_path,
                    "code": code
                })

    return source_files


def main():
    source_files = load_source_files()

    print("Total source files loaded:", len(source_files))

    for file in source_files[:3]:
        print("\nRepository:", file["repository"])
        print("File:", file["file_path"])
        print("Code:")
        print(file["code"][:200])


if __name__ == "__main__":
    main()