import os
import csv
import subprocess
from collections import Counter


class RepositoryMiner:

    def __init__(self):
        self.repositories = {
            "flask": r"C:\Users\ashmi\Desktop\Special Topics Devops\flask",
            "requests": r"C:\Users\ashmi\Desktop\Special Topics Devops\requests",
            "pytest": r"C:\Users\ashmi\Desktop\Special Topics Devops\pytest",
            "fastapi": r"C:\Users\ashmi\Desktop\Special Topics Devops\fastapi",
            "scikit-learn": r"C:\Users\ashmi\Desktop\Special Topics Devops\scikit-learn"
        }

        self.source_data = []
        self.commit_data = []

    def get_language(self, extension):
        languages = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".java": "Java",
            ".cpp": "C++",
            ".c": "C",
            ".h": "C/C++ Header",
            ".hpp": "C++ Header",
            ".go": "Go",
            ".rs": "Rust",
            ".rb": "Ruby",
            ".php": "PHP",
            ".html": "HTML",
            ".css": "CSS",
            ".sh": "Shell"
        }

        return languages.get(extension.lower())

    def count_loc(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return sum(1 for line in file if line.strip())
        except (UnicodeDecodeError, PermissionError):
            return 0

    def scan_source_code(self):
        print("\n===== SOURCE CODE MINING =====")

        for repo_name, repo_path in self.repositories.items():

            print(f"Analyzing: {repo_name}")

            for root, dirs, files in os.walk(repo_path):

                if ".git" in dirs:
                    dirs.remove(".git")

                for file in files:

                    extension = os.path.splitext(file)[1].lower()
                    language = self.get_language(extension)

                    if language is None:
                        continue

                    file_path = os.path.join(root, file)
                    loc = self.count_loc(file_path)

                    try:
                        size = os.path.getsize(file_path)
                    except OSError:
                        size = 0

                    relative_path = os.path.relpath(file_path, repo_path)

                    self.source_data.append({
                        "repository": repo_name,
                        "file_path": relative_path,
                        "language": language,
                        "extension": extension,
                        "loc": loc,
                        "size_bytes": size
                    })

            print(f"Completed: {repo_name}")

    def save_source_dataset(self):
        output_file = r"C:\Users\ashmi\Desktop\Special Topics Devops\CSET456Lab\lab2\data\source_code_dataset.csv"

        fields = [
            "repository",
            "file_path",
            "language",
            "extension",
            "loc",
            "size_bytes"
        ]

        with open(output_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)

            writer.writeheader()
            writer.writerows(self.source_data)

        print("\nSource code dataset saved to:")
        print(output_file)

    def source_statistics(self):
        repositories = Counter()
        languages = Counter()

        for row in self.source_data:
            repositories[row["repository"]] += 1
            languages[row["language"]] += 1

        print("\n===== SOURCE CODE STATISTICS =====")
        print("Total source files:", len(self.source_data))

        print("\nFiles per repository:")
        for repo, count in repositories.items():
            print(repo, ":", count)

        print("\nLanguages:")
        for language, count in languages.items():
            print(language, ":", count)

    def mine_commit_history(self):
        print("\n===== COMMIT HISTORY MINING =====")

        for repo_name, repo_path in self.repositories.items():

            print(f"Analyzing commits: {repo_name}")

            command = [
                "git",
                "-C",
                repo_path,
                "log",
                "--numstat",
                "--pretty=format:COMMIT|%H|%an|%aI"
            ]

            try:
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace"
                )

                lines = result.stdout.splitlines()

                commit_hash = ""
                author = ""
                date = ""
                files_changed = 0
                additions = 0
                deletions = 0
                commit_count = 0

                for line in lines:

                    if line.startswith("COMMIT|"):

                        if commit_hash:
                            self.commit_data.append({
                                "repository": repo_name,
                                "commit_hash": commit_hash,
                                "author": author,
                                "date": date,
                                "files_changed": files_changed,
                                "additions": additions,
                                "deletions": deletions
                            })

                        parts = line.split("|")

                        commit_hash = parts[1]
                        author = parts[2]
                        date = parts[3][:10]

                        files_changed = 0
                        additions = 0
                        deletions = 0

                        commit_count += 1

                        if commit_count % 500 == 0:
                            print(f"  Processed {commit_count} commits...")

                    else:

                        parts = line.split("\t")

                        if len(parts) >= 3:

                            added = parts[0]
                            deleted = parts[1]

                            if added.isdigit():
                                additions += int(added)

                            if deleted.isdigit():
                                deletions += int(deleted)

                            files_changed += 1

                if commit_hash:
                    self.commit_data.append({
                        "repository": repo_name,
                        "commit_hash": commit_hash,
                        "author": author,
                        "date": date,
                        "files_changed": files_changed,
                        "additions": additions,
                        "deletions": deletions
                    })

                print(f"Completed commits: {repo_name} ({commit_count})")

            except Exception as e:
                print(f"Error while processing {repo_name}: {e}")

    def save_commit_dataset(self):
        output_file = r"C:\Users\ashmi\Desktop\Special Topics Devops\CSET456Lab\lab2\data\commit_history_dataset.csv"

        fields = [
            "repository",
            "commit_hash",
            "author",
            "date",
            "files_changed",
            "additions",
            "deletions"
        ]

        with open(output_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)

            writer.writeheader()
            writer.writerows(self.commit_data)

        print("\nCommit history dataset saved to:")
        print(output_file)

    def commit_statistics(self):
        repositories = Counter()
        authors = Counter()

        total_additions = 0
        total_deletions = 0

        for row in self.commit_data:

            repositories[row["repository"]] += 1
            authors[row["author"]] += 1

            total_additions += row["additions"]
            total_deletions += row["deletions"]

        print("\n===== COMMIT HISTORY STATISTICS =====")

        print("Total commits:", len(self.commit_data))

        print("\nCommits per repository:")
        for repo, count in repositories.items():
            print(repo, ":", count)

        print("\nTotal contributors:", len(authors))

        if authors:
            print(
                "Most active contributor:",
                authors.most_common(1)[0][0]
            )

        print("Total additions:", total_additions)
        print("Total deletions:", total_deletions)

    def run(self):

        self.scan_source_code()
        self.save_source_dataset()
        self.source_statistics()

        self.mine_commit_history()
        self.save_commit_dataset()
        self.commit_statistics()


def main():
    miner = RepositoryMiner()
    miner.run()


if __name__ == "__main__":
    main()