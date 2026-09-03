import os
import csv
import json
from collections import Counter, defaultdict
from pydriller import Repository


REPO_PATH = r"C:\Users\ashmi\Desktop\Special Topics Devops\flask"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LAB_DIR = os.path.dirname(BASE_DIR)

DATA_DIR = os.path.join(LAB_DIR, "data")
OUTPUT_DIR = os.path.join(LAB_DIR, "output")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


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


def get_language(extension):
    return LANGUAGES.get(extension.lower(), "Other")


# ==============================
# TASK 1: REPOSITORY INVENTORY
# ==============================

total_files = 0
total_directories = 0
source_files = 0
total_loc = 0

file_types = Counter()
languages = Counter()
file_metrics = []
largest_files = []


for root, dirs, files in os.walk(REPO_PATH):

    dirs[:] = [d for d in dirs if d != ".git"]

    total_directories += len(dirs)

    for filename in files:

        total_files += 1

        extension = os.path.splitext(filename)[1].lower()

        if extension:
            file_types[extension] += 1
        else:
            file_types["[no extension]"] += 1

        if extension not in LANGUAGES:
            continue

        source_files += 1

        language = get_language(extension)
        file_path = os.path.join(root, filename)

        try:
            size = os.path.getsize(file_path)

            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:
                loc = sum(1 for line in f if line.strip())

            relative_path = os.path.relpath(
                file_path,
                REPO_PATH
            ).replace("\\", "/")

            file_metrics.append([
                relative_path,
                language,
                extension,
                loc,
                size
            ])

            languages[language] += 1
            total_loc += loc

            largest_files.append({
                "file": relative_path,
                "loc": loc
            })

        except Exception as e:
            print("Could not read:", file_path)


largest_files = sorted(
    largest_files,
    key=lambda x: x["loc"],
    reverse=True
)[:5]


# ==============================
# CREATE FILE METRICS CSV
# ==============================

file_csv = os.path.join(DATA_DIR, "file_metrics.csv")

with open(file_csv, "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "file_path",
        "language",
        "extension",
        "loc",
        "size_bytes"
    ])

    writer.writerows(file_metrics)


# ==============================
# TASK 3: MINE GIT HISTORY
# ==============================

total_commits = 0

contributors = Counter()
changed_files = Counter()

commits_per_month = Counter()
files_per_month = defaultdict(int)
additions_per_month = defaultdict(int)
deletions_per_month = defaultdict(int)

total_additions = 0
total_deletions = 0
total_files_changed = 0


print("Mining Git history... Please wait.")


for commit in Repository(REPO_PATH).traverse_commits():

    total_commits += 1

    author = commit.author.name
    contributors[author] += 1

    month = commit.author_date.strftime("%Y-%m")

    commits_per_month[month] += 1

    for modification in commit.modified_files:

        filename = modification.new_path or modification.old_path

        if filename:
            changed_files[filename] += 1
            files_per_month[month] += 1
            total_files_changed += 1

        total_additions += modification.added_lines
        total_deletions += modification.deleted_lines

        additions_per_month[month] += modification.added_lines
        deletions_per_month[month] += modification.deleted_lines


# ==============================
# CALCULATE GIT STATISTICS
# ==============================

most_active_contributor = (
    contributors.most_common(1)[0]
    if contributors
    else ("None", 0)
)

most_changed_files = changed_files.most_common(5)

average_files_changed_per_commit = (
    total_files_changed / total_commits
    if total_commits else 0
)

average_additions_per_commit = (
    total_additions / total_commits
    if total_commits else 0
)

average_deletions_per_commit = (
    total_deletions / total_commits
    if total_commits else 0
)


# ==============================
# CREATE MONTHLY GIT CSV
# ==============================

monthly_csv = os.path.join(
    DATA_DIR,
    "monthly_git_metrics.csv"
)

with open(monthly_csv, "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "month",
        "commits",
        "total_files_changed",
        "average_files_changed",
        "additions",
        "deletions"
    ])

    for month in sorted(commits_per_month):

        commits = commits_per_month[month]
        files = files_per_month[month]

        average_files = files / commits if commits else 0

        writer.writerow([
            month,
            commits,
            files,
            round(average_files, 2),
            additions_per_month[month],
            deletions_per_month[month]
        ])


# ==============================
# CREATE FINAL JSON
# ==============================

statistics = {
    "repository_name": os.path.basename(REPO_PATH),

    "repository_inventory": {
        "total_files": total_files,
        "source_code_files": source_files,
        "directories": total_directories,
        "total_loc": total_loc,
        "languages": dict(languages),
        "file_type_distribution": dict(file_types),
        "largest_source_files": largest_files
    },

    "git_history": {
        "total_commits": total_commits,
        "number_of_contributors": len(contributors),

        "most_active_contributor": {
            "name": most_active_contributor[0],
            "commits": most_active_contributor[1]
        },

        "most_frequently_changed_files": [
            {
                "file": file,
                "changes": count
            }
            for file, count in most_changed_files
        ],

        "commits_per_month": dict(
            sorted(commits_per_month.items())
        ),

        "average_files_changed_per_commit": round(
            average_files_changed_per_commit, 2
        ),

        "average_additions_per_commit": round(
            average_additions_per_commit, 2
        ),

        "average_deletions_per_commit": round(
            average_deletions_per_commit, 2
        )
    }
}


json_file = os.path.join(
    OUTPUT_DIR,
    "repository_statistics.json"
)

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(statistics, f, indent=4)


# ==============================
# PRINT SUMMARY
# ==============================

print("\n===== REPOSITORY INVENTORY =====")
print("Repository:", statistics["repository_name"])
print("Total files:", total_files)
print("Source files:", source_files)
print("Directories:", total_directories)
print("Total LOC:", total_loc)

print("\nLanguages:")
for language, count in languages.items():
    print(language, ":", count)

print("\n===== GIT HISTORY =====")
print("Total commits:", total_commits)
print("Contributors:", len(contributors))

print(
    "Most active contributor:",
    most_active_contributor[0],
    f"({most_active_contributor[1]} commits)"
)

print("\nTop 5 most frequently changed files:")
for file, count in most_changed_files:
    print(file, ":", count)

print(
    "\nAverage files changed per commit:",
    round(average_files_changed_per_commit, 2)
)

print(
    "Average additions per commit:",
    round(average_additions_per_commit, 2)
)

print(
    "Average deletions per commit:",
    round(average_deletions_per_commit, 2)
)

print("\n===== GENERATED FILES =====")
print(file_csv)
print(monthly_csv)
print(json_file)