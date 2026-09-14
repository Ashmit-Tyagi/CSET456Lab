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
        self.merged_data = []

        self.data_path = (
            r"C:\Users\ashmi\Desktop\Special Topics Devops"
            r"\CSET456Lab\lab2\data"
        )

    # ---------------- SOURCE CODE ----------------

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
            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                return sum(
                    1 for line in file
                    if line.strip()
                )

        except Exception:
            return 0

    def scan_source_code(self):

        print("\n===== SOURCE CODE MINING =====")

        for repo_name, repo_path in self.repositories.items():

            print(f"Analyzing: {repo_name}")

            for root, dirs, files in os.walk(repo_path):

                if ".git" in dirs:
                    dirs.remove(".git")

                for file_name in files:

                    extension = os.path.splitext(
                        file_name
                    )[1]

                    language = self.get_language(extension)

                    if language is None:
                        continue

                    file_path = os.path.join(
                        root,
                        file_name
                    )

                    try:

                        size = os.path.getsize(
                            file_path
                        )

                        loc = self.count_loc(
                            file_path
                        )

                        self.source_data.append({
                            "repository": repo_name,
                            "file_path": os.path.relpath(
                                file_path,
                                repo_path
                            ),
                            "language": language,
                            "extension": extension,
                            "loc": loc,
                            "size_bytes": size
                        })

                    except Exception:
                        continue

            print(f"Completed: {repo_name}")

    def save_source_dataset(self):

        path = os.path.join(
            self.data_path,
            "source_code_dataset.csv"
        )

        fields = [
            "repository",
            "file_path",
            "language",
            "extension",
            "loc",
            "size_bytes"
        ]

        with open(
            path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fields
            )

            writer.writeheader()
            writer.writerows(
                self.source_data
            )

        print("\nSource code dataset saved to:")
        print(path)

    def source_statistics(self):

        print("\n===== SOURCE CODE STATISTICS =====")

        print(
            f"Total source files: "
            f"{len(self.source_data)}"
        )

        repo_count = Counter(
            row["repository"]
            for row in self.source_data
        )

        print("\nFiles per repository:")

        for repo, count in repo_count.items():
            print(f"{repo} : {count}")

        language_count = Counter(
            row["language"]
            for row in self.source_data
        )

        print("\nLanguages:")

        for language, count in language_count.items():
            print(f"{language} : {count}")

    # ---------------- COMMIT HISTORY ----------------

    def mine_commit_history(self):

        print("\n===== COMMIT HISTORY MINING =====")

        for repo_name, repo_path in self.repositories.items():

            print(
                f"Analyzing commits: "
                f"{repo_name}"
            )

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
                            print(
                                f"  Processed "
                                f"{commit_count} commits..."
                            )

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

                print(
                    f"Completed commits: "
                    f"{repo_name} ({commit_count})"
                )

            except Exception as e:

                print(
                    f"Error while processing "
                    f"{repo_name}: {e}"
                )

    def save_commit_dataset(self):

        path = os.path.join(
            self.data_path,
            "commit_history_dataset.csv"
        )

        fields = [
            "repository",
            "commit_hash",
            "author",
            "date",
            "files_changed",
            "additions",
            "deletions"
        ]

        with open(
            path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fields
            )

            writer.writeheader()
            writer.writerows(
                self.commit_data
            )

        print(
            "\nCommit history dataset saved to:"
        )

        print(path)

    def commit_statistics(self):

        print(
            "\n===== COMMIT HISTORY STATISTICS ====="
        )

        print(
            f"Total commits: "
            f"{len(self.commit_data)}"
        )

        repo_count = Counter(
            row["repository"]
            for row in self.commit_data
        )

        print("\nCommits per repository:")

        for repo, count in repo_count.items():
            print(f"{repo} : {count}")

        contributors = set(
            row["author"]
            for row in self.commit_data
            if row["author"]
        )

        total_additions = sum(
            int(row["additions"])
            for row in self.commit_data
        )

        total_deletions = sum(
            int(row["deletions"])
            for row in self.commit_data
        )

        print(
            f"\nTotal contributors: "
            f"{len(contributors)}"
        )

        print(
            f"Total additions: "
            f"{total_additions}"
        )

        print(
            f"Total deletions: "
            f"{total_deletions}"
        )

    # ---------------- DATA CLEANING ----------------

    def clean_datasets(self):

        print("\n===== DATA CLEANING =====")

        cleaned_source = []
        seen_files = set()

        for row in self.source_data:

            key = (
                row["repository"],
                row["file_path"]
            )

            if (
                row["repository"]
                and row["file_path"]
                and row["language"]
                and int(row["loc"]) >= 0
                and int(row["size_bytes"]) >= 0
                and key not in seen_files
            ):

                cleaned_source.append(row)
                seen_files.add(key)

        self.source_data = cleaned_source

        cleaned_commits = []
        seen_commits = set()

        for row in self.commit_data:

            commit_hash = row["commit_hash"]

            if (
                row["repository"]
                and commit_hash
                and row["author"]
                and row["date"]
                and commit_hash not in seen_commits
            ):

                cleaned_commits.append(row)
                seen_commits.add(commit_hash)

        self.commit_data = cleaned_commits

        print(
            f"Clean source records: "
            f"{len(self.source_data)}"
        )

        print(
            f"Clean commit records: "
            f"{len(self.commit_data)}"
        )

    def save_cleaned_datasets(self):

        source_path = os.path.join(
            self.data_path,
            "cleaned_source_code_dataset.csv"
        )

        source_fields = [
            "repository",
            "file_path",
            "language",
            "extension",
            "loc",
            "size_bytes"
        ]

        with open(
            source_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=source_fields
            )

            writer.writeheader()
            writer.writerows(
                self.source_data
            )

        commit_path = os.path.join(
            self.data_path,
            "cleaned_commit_history_dataset.csv"
        )

        commit_fields = [
            "repository",
            "commit_hash",
            "author",
            "date",
            "files_changed",
            "additions",
            "deletions"
        ]

        with open(
            commit_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=commit_fields
            )

            writer.writeheader()
            writer.writerows(
                self.commit_data
            )

        print("\nCleaned datasets saved:")
        print(source_path)
        print(commit_path)

    # ---------------- MERGED DATASET ----------------

    def create_merged_dataset(self):

        print("\n===== CREATING MERGED DATASET =====")

        source_summary = {}
        commit_summary = {}

        # Aggregate source code data

        for row in self.source_data:

            repo = row["repository"]

            if repo not in source_summary:

                source_summary[repo] = {
                    "source_files": 0,
                    "total_loc": 0
                }

            source_summary[repo]["source_files"] += 1

            source_summary[repo]["total_loc"] += int(
                row["loc"]
            )

        # Aggregate commit data

        for row in self.commit_data:

            repo = row["repository"]

            if repo not in commit_summary:

                commit_summary[repo] = {
                    "total_commits": 0,
                    "contributors": set(),
                    "total_additions": 0,
                    "total_deletions": 0,
                    "total_files_changed": 0
                }

            commit_summary[repo]["total_commits"] += 1

            commit_summary[repo]["contributors"].add(
                row["author"]
            )

            commit_summary[repo]["total_additions"] += int(
                row["additions"]
            )

            commit_summary[repo]["total_deletions"] += int(
                row["deletions"]
            )

            commit_summary[repo]["total_files_changed"] += int(
                row["files_changed"]
            )

        # Merge both datasets

        for repo in self.repositories:

            source = source_summary.get(
                repo,
                {
                    "source_files": 0,
                    "total_loc": 0
                }
            )

            commits = commit_summary.get(
                repo,
                {
                    "total_commits": 0,
                    "contributors": set(),
                    "total_additions": 0,
                    "total_deletions": 0,
                    "total_files_changed": 0
                }
            )

            source_files = source["source_files"]
            total_loc = source["total_loc"]
            total_commits = commits["total_commits"]

            if source_files > 0:
                average_loc = round(
                    total_loc / source_files,
                    2
                )
            else:
                average_loc = 0

            if total_commits > 0:
                average_files_changed = round(
                    commits["total_files_changed"]
                    / total_commits,
                    2
                )
            else:
                average_files_changed = 0

            self.merged_data.append({
                "repository": repo,
                "source_files": source_files,
                "total_loc": total_loc,
                "average_loc": average_loc,
                "total_commits": total_commits,
                "contributors": len(
                    commits["contributors"]
                ),
                "total_additions": commits[
                    "total_additions"
                ],
                "total_deletions": commits[
                    "total_deletions"
                ],
                "average_files_changed": average_files_changed
            })

        print(
            f"Merged records: "
            f"{len(self.merged_data)}"
        )

    def save_merged_dataset(self):

        path = os.path.join(
            self.data_path,
            "merged_repository_dataset.csv"
        )

        fields = [
            "repository",
            "source_files",
            "total_loc",
            "average_loc",
            "total_commits",
            "contributors",
            "total_additions",
            "total_deletions",
            "average_files_changed"
        ]

        with open(
            path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fields
            )

            writer.writeheader()
            writer.writerows(
                self.merged_data
            )

        print(
            "\nMerged dataset saved to:"
        )

        print(path)

    def merged_statistics(self):

        print(
            "\n===== MERGED DATASET STATISTICS ====="
        )

        print(
            f"Total repositories: "
            f"{len(self.merged_data)}"
        )

        for row in self.merged_data:

            print(
                f"\n{row['repository']}"
            )

            print(
                f"  Source files: "
                f"{row['source_files']}"
            )

            print(
                f"  Total LOC: "
                f"{row['total_loc']}"
            )

            print(
                f"  Average LOC: "
                f"{row['average_loc']}"
            )

            print(
                f"  Total commits: "
                f"{row['total_commits']}"
            )

            print(
                f"  Contributors: "
                f"{row['contributors']}"
            )

            print(
                f"  Additions: "
                f"{row['total_additions']}"
            )

            print(
                f"  Deletions: "
                f"{row['total_deletions']}"
            )

            print(
                f"  Average files changed: "
                f"{row['average_files_changed']}"
            )

    # ---------------- RUN ----------------

    def run(self):

        self.scan_source_code()
        self.save_source_dataset()
        self.source_statistics()

        self.mine_commit_history()
        self.save_commit_dataset()
        self.commit_statistics()

        self.clean_datasets()
        self.save_cleaned_datasets()

        self.create_merged_dataset()
        self.save_merged_dataset()
        self.merged_statistics()


def main():

    miner = RepositoryMiner()
    miner.run()


if __name__ == "__main__":
    main()