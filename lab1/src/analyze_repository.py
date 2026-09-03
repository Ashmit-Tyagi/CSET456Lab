import os
import csv
import json
from collections import Counter, defaultdict
from pydriller import Repository


REPO_PATH = r"C:\Users\ashmi\Desktop\Special Topics Devops\flask"


class RepositoryAnalyzer:

    LANGUAGES = {
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
        ".sh": "Shell",
    }

    def __init__(self, repo_path):

        self.repo_path = repo_path

        self.base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        self.lab_dir = os.path.dirname(self.base_dir)

        self.data_dir = os.path.join(
            self.lab_dir,
            "data"
        )

        self.output_dir = os.path.join(
            self.lab_dir,
            "output"
        )

        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

        # Repository metrics
        self.total_files = 0
        self.total_directories = 0
        self.source_files = 0
        self.total_loc = 0

        self.file_types = Counter()
        self.languages = Counter()
        self.file_metrics = []
        self.largest_files = []

        # Git metrics
        self.total_commits = 0
        self.contributors = Counter()
        self.changed_files = Counter()

        self.commits_per_month = Counter()
        self.files_per_month = defaultdict(int)
        self.additions_per_month = defaultdict(int)
        self.deletions_per_month = defaultdict(int)

        self.total_additions = 0
        self.total_deletions = 0
        self.total_files_changed = 0

    # ---------------------------------
    # SOURCE CODE ANALYSIS
    # ---------------------------------

    def get_language(self, extension):
        return self.LANGUAGES.get(
            extension.lower(),
            "Other"
        )

    def count_loc(self, file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            return sum(
                1 for line in file
                if line.strip()
            )

    def analyze_file(self, root, filename):

        extension = os.path.splitext(
            filename
        )[1].lower()

        if extension:
            self.file_types[extension] += 1
        else:
            self.file_types["[no extension]"] += 1

        if extension not in self.LANGUAGES:
            return

        file_path = os.path.join(
            root,
            filename
        )

        try:

            size = os.path.getsize(file_path)
            loc = self.count_loc(file_path)

            relative_path = os.path.relpath(
                file_path,
                self.repo_path
            ).replace("\\", "/")

            language = self.get_language(extension)

            self.file_metrics.append([
                relative_path,
                language,
                extension,
                loc,
                size
            ])

            self.languages[language] += 1
            self.source_files += 1
            self.total_loc += loc

            self.largest_files.append({
                "file": relative_path,
                "loc": loc
            })

        except Exception:
            print("Could not read:", file_path)

    def scan_repository(self):

        print("Scanning repository...")

        for root, dirs, files in os.walk(
            self.repo_path
        ):

            dirs[:] = [
                d for d in dirs
                if d != ".git"
            ]

            self.total_directories += len(dirs)

            for filename in files:

                self.total_files += 1

                self.analyze_file(
                    root,
                    filename
                )

        self.largest_files = sorted(
            self.largest_files,
            key=lambda x: x["loc"],
            reverse=True
        )[:5]

    # ---------------------------------
    # CSV OUTPUT
    # ---------------------------------

    def create_file_metrics_csv(self):

        file_path = os.path.join(
            self.data_dir,
            "file_metrics.csv"
        )

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "file_path",
                "language",
                "extension",
                "loc",
                "size_bytes"
            ])

            writer.writerows(
                self.file_metrics
            )

        print("Created:", file_path)

    # ---------------------------------
    # GIT HISTORY ANALYSIS
    # ---------------------------------

    def mine_git_history(self):

        print("Mining Git history... Please wait.")

        for commit in Repository(
            self.repo_path
        ).traverse_commits():

            self.total_commits += 1

            author = commit.author.name

            self.contributors[author] += 1

            month = commit.author_date.strftime(
                "%Y-%m"
            )

            self.commits_per_month[month] += 1

            for modification in commit.modified_files:

                filename = (
                    modification.new_path
                    or modification.old_path
                )

                if filename:

                    self.changed_files[
                        filename
                    ] += 1

                    self.files_per_month[
                        month
                    ] += 1

                    self.total_files_changed += 1

                self.total_additions += (
                    modification.added_lines
                )

                self.total_deletions += (
                    modification.deleted_lines
                )

                self.additions_per_month[
                    month
                ] += modification.added_lines

                self.deletions_per_month[
                    month
                ] += modification.deleted_lines

    # ---------------------------------
    # GIT STATISTICS
    # ---------------------------------

    def calculate_git_statistics(self):

        most_active = (
            self.contributors.most_common(1)[0]
            if self.contributors
            else ("None", 0)
        )

        most_changed = (
            self.changed_files.most_common(5)
        )

        average_files = (
            self.total_files_changed
            / self.total_commits
            if self.total_commits
            else 0
        )

        average_additions = (
            self.total_additions
            / self.total_commits
            if self.total_commits
            else 0
        )

        average_deletions = (
            self.total_deletions
            / self.total_commits
            if self.total_commits
            else 0
        )

        return {
            "most_active_contributor": most_active,
            "most_changed_files": most_changed,
            "average_files_changed": average_files,
            "average_additions": average_additions,
            "average_deletions": average_deletions
        }

    # ---------------------------------
    # MONTHLY CSV
    # ---------------------------------

    def create_monthly_csv(self):

        file_path = os.path.join(
            self.data_dir,
            "monthly_git_metrics.csv"
        )

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "month",
                "commits",
                "total_files_changed",
                "average_files_changed",
                "additions",
                "deletions"
            ])

            for month in sorted(
                self.commits_per_month
            ):

                commits = (
                    self.commits_per_month[month]
                )

                files = (
                    self.files_per_month[month]
                )

                average_files = (
                    files / commits
                    if commits
                    else 0
                )

                writer.writerow([
                    month,
                    commits,
                    files,
                    round(
                        average_files,
                        2
                    ),
                    self.additions_per_month[
                        month
                    ],
                    self.deletions_per_month[
                        month
                    ]
                ])

        print("Created:", file_path)

    # ---------------------------------
    # JSON OUTPUT
    # ---------------------------------

    def create_json(self):

        git_stats = (
            self.calculate_git_statistics()
        )

        statistics = {

            "repository_name":
                os.path.basename(
                    self.repo_path
                ),

            "repository_inventory": {

                "total_files":
                    self.total_files,

                "source_code_files":
                    self.source_files,

                "directories":
                    self.total_directories,

                "total_loc":
                    self.total_loc,

                "languages":
                    dict(self.languages),

                "file_type_distribution":
                    dict(self.file_types),

                "largest_source_files":
                    self.largest_files
            },

            "git_history": {

                "total_commits":
                    self.total_commits,

                "number_of_contributors":
                    len(self.contributors),

                "most_active_contributor": {

                    "name":
                        git_stats[
                            "most_active_contributor"
                        ][0],

                    "commits":
                        git_stats[
                            "most_active_contributor"
                        ][1]
                },

                "most_frequently_changed_files": [

                    {
                        "file": file,
                        "changes": count
                    }

                    for file, count
                    in git_stats[
                        "most_changed_files"
                    ]
                ],

                "commits_per_month":
                    dict(
                        sorted(
                            self.commits_per_month.items()
                        )
                    ),

                "average_files_changed_per_commit":
                    round(
                        git_stats[
                            "average_files_changed"
                        ],
                        2
                    ),

                "average_additions_per_commit":
                    round(
                        git_stats[
                            "average_additions"
                        ],
                        2
                    ),

                "average_deletions_per_commit":
                    round(
                        git_stats[
                            "average_deletions"
                        ],
                        2
                    )
            }
        }

        file_path = os.path.join(
            self.output_dir,
            "repository_statistics.json"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                statistics,
                file,
                indent=4
            )

        print("Created:", file_path)

    # ---------------------------------
    # SUMMARY
    # ---------------------------------

    def print_summary(self):

        git_stats = (
            self.calculate_git_statistics()
        )

        print("\n===== REPOSITORY INVENTORY =====")

        print(
            "Repository:",
            os.path.basename(
                self.repo_path
            )
        )

        print(
            "Total files:",
            self.total_files
        )

        print(
            "Source files:",
            self.source_files
        )

        print(
            "Directories:",
            self.total_directories
        )

        print(
            "Total LOC:",
            self.total_loc
        )

        print("\nLanguages:")

        for language, count in (
            self.languages.items()
        ):

            print(
                language,
                ":",
                count
            )

        print("\n===== GIT HISTORY =====")

        print(
            "Total commits:",
            self.total_commits
        )

        print(
            "Contributors:",
            len(self.contributors)
        )

        print(
            "Most active contributor:",
            git_stats[
                "most_active_contributor"
            ][0],
            f"({git_stats['most_active_contributor'][1]} commits)"
        )

        print(
            "\nAverage files changed per commit:",
            round(
                git_stats[
                    "average_files_changed"
                ],
                2
            )
        )

        print(
            "Average additions per commit:",
            round(
                git_stats[
                    "average_additions"
                ],
                2
            )
        )

        print(
            "Average deletions per commit:",
            round(
                git_stats[
                    "average_deletions"
                ],
                2
            )
        )

    # ---------------------------------
    # RUN EVERYTHING
    # ---------------------------------

    def run(self):

        self.scan_repository()

        self.create_file_metrics_csv()

        self.mine_git_history()

        self.create_monthly_csv()

        self.create_json()

        self.print_summary()


def main():

    analyzer = RepositoryAnalyzer(
        REPO_PATH
    )

    analyzer.run()


if __name__ == "__main__":
    main()