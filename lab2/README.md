# Lab 2 - Repository Mining and Dataset Analysis

## 1. Objective

The objective of this lab is to mine multiple open-source GitHub repositories and create useful datasets from their source code and Git commit history.

For this lab, five repositories were analyzed:

1. Flask
2. Requests
3. Pytest
4. FastAPI
5. Scikit-learn

The main goal was to understand what information can be extracted from a software repository and how this information can be converted into datasets for further analysis.

---

## 2. Repositories Used

| Repository   | Description                   |
| ------------ | ----------------------------- |
| Flask        | Python web framework          |
| Requests     | Python HTTP library           |
| Pytest       | Python testing framework      |
| FastAPI      | Python web framework for APIs |
| Scikit-learn | Machine learning library      |

---

## 3. Technology Stack

The following technologies were used:

* **Python** - Main programming language
* **PyDriller** - Repository mining and Git analysis
* **Git** - Accessing repository commit history
* **CSV** - Storing datasets
* **JSON** - Storing statistics
* **GitHub** - Source repositories and version control
* **VS Code** - Development and documentation

---

## 4. Applications Used and Their Association with the Project

### GitHub

GitHub was used as the source of the five open-source repositories. The repositories contain source code and complete Git histories that were mined for this project.

### Git

Git was used to access the commit history of each repository. Commit information such as commit hash, author, date, additions, deletions and files changed was extracted.

### Python

Python was used to build the repository mining program and process the collected data.

### PyDriller

PyDriller was used as the repository mining library. It provides access to Git repository information and helped in understanding repository mining concepts.

### CSV

CSV files were used to store the extracted source-code and commit-history datasets because they are simple to inspect and can easily be used for data analysis.

### JSON

JSON files were used to store statistical summaries of the three datasets.

---

# 5. Dataset 1 - Source Code Dataset

The source-code dataset contains information about the source files present in each repository.

### Features

The following features were extracted:

* Repository name
* File path
* Programming language
* File extension
* Lines of code
* File size in bytes

### Why these features were selected

These features are useful for understanding the structure and size of a software project.

For example:

* **Repository** identifies the project.
* **File path** identifies the location of a file.
* **Language** tells us which programming language is being used.
* **LOC** gives an estimate of the amount of source code.
* **File size** provides another measure of file size.

### Source Code Dataset Results

A total of **2668 source files** were collected from the five repositories.

| Repository   | Source Files | Total LOC |
| ------------ | -----------: | --------: |
| Flask        |          106 |    14,528 |
| Requests     |           39 |     9,875 |
| Pytest       |          276 |    98,115 |
| FastAPI      |        1,155 |    98,537 |
| Scikit-learn |        1,092 |   386,608 |

The dataset contained mainly Python files, along with smaller amounts of JavaScript, TypeScript-related files, HTML, CSS, C/C++ and shell files.

---

# 6. Dataset 2 - Commit History Dataset

The second dataset contains information extracted from the Git history of the repositories.

### Features

The following information was collected:

* Repository name
* Commit hash
* Author
* Commit date
* Number of files changed
* Number of additions
* Number of deletions

### Commit History Results

A total of **71,512 commits** were collected.

| Repository   | Commits | Contributors |
| ------------ | ------: | -----------: |
| Flask        |   5,556 |          858 |
| Requests     |   6,494 |          790 |
| Pytest       |  17,752 |        1,171 |
| FastAPI      |   7,713 |          911 |
| Scikit-learn |  33,997 |        3,528 |

The dataset provides information about the development activity and collaboration history of each repository.

---

# 7. Data Cleaning

Before creating the final dataset, the extracted data was checked for invalid or unnecessary records.

### Source-code dataset checks

* Repository name should not be empty.
* File path should not be empty.
* Programming language should be identified.
* LOC should not be negative.
* File size should not be negative.
* Duplicate repository/file combinations were checked.

### Commit-history dataset checks

* Repository name should not be empty.
* Commit hash should not be empty.
* Author should not be empty.
* Commit date should not be empty.
* Duplicate commits were checked.

After validation:

* **2668 clean source-code records**
* **71,512 clean commit-history records**

No valid records had to be removed during cleaning.

This was important because cleaning should not mean deleting data unnecessarily. The purpose was to check whether the extracted information was valid and relevant.

---

# 8. Dataset 3 - Merged Repository Dataset

The source-code and commit-history datasets contain information at different levels.

The source dataset contains information about individual files, while the commit dataset contains information about individual commits.

Directly joining these two datasets would create repeated and unnecessary records.

Therefore, both datasets were first summarized at the **repository level** and then merged.

### Features

The merged dataset contains:

* Repository
* Number of source files
* Total LOC
* Average LOC
* Total commits
* Number of contributors
* Total additions
* Total deletions
* Average files changed per commit

### Merged Dataset

| Repository   | Source Files | Total LOC | Commits | Contributors |
| ------------ | -----------: | --------: | ------: | -----------: |
| Flask        |          106 |    14,528 |   5,556 |          858 |
| Requests     |           39 |     9,875 |   6,494 |          790 |
| Pytest       |          276 |    98,115 |  17,752 |        1,171 |
| FastAPI      |        1,155 |    98,537 |   7,713 |          911 |
| Scikit-learn |        1,092 |   386,608 |  33,997 |        3,528 |

The merged dataset provides a higher-level view of both the codebase and its development history.

---

# 9. Dataset Statistics

Three separate JSON files were generated:

```text
output/
├── source_code_statistics.json
├── commit_history_statistics.json
└── merged_dataset_statistics.json
```

These files contain statistical summaries of the corresponding datasets.

They make it easier to use the mined information without processing the complete CSV files again.

---

# 10. Analysis of the Datasets

### Source Code Dataset

The source-code dataset can be used to understand the size and structure of different software projects.

For example, Scikit-learn has a much larger total LOC than Flask and Requests. FastAPI has a large number of source files but a lower average LOC per file.

This shows that the number of files alone does not always represent the size of a codebase.

### Commit History Dataset

The commit dataset gives information about development activity.

Scikit-learn has the highest number of commits and contributors among the five repositories in this dataset.

The additions and deletions can also provide an idea of how much code has changed throughout the project's history.

### Merged Dataset

The merged dataset allows source-code information and development-history information to be studied together.

This makes the merged dataset more useful for repository-level comparisons.

---

# 11. Problems / Applications Where These Datasets Can Be Used

The datasets created in this lab can be useful for several software engineering problems.

### 1. Codebase Size Analysis

The source-code dataset can be used to identify large repositories or files.

It can help answer questions such as:

* Which repository contains the most source code?
* Which files are very large?
* Which programming languages are used?

### 2. Repository Activity Analysis

The commit dataset can be used to study project development activity.

Possible questions include:

* How active is a repository?
* How many contributors are involved?
* How frequently are changes made?
* How much code is added or deleted?

### 3. Developer Contribution Analysis

Commit information can be used to analyze contributor participation.

For example, it can help identify:

* Number of contributors
* Contributions over time
* Frequently active contributors

### 4. Code Maintenance

Combining source-code size with commit activity can help identify repositories or areas of a project that require frequent changes.

This information could potentially be used for maintenance planning.

### 5. Repository Comparison

The merged dataset can be used to compare different open-source projects using common measurements such as:

* Source files
* LOC
* Commits
* Contributors
* Additions
* Deletions

---

# 12. Repository Health Snapshot

The merged dataset can be viewed as a simple **Repository Health Snapshot**.

Instead of looking at thousands of individual commits and files, a repository can be represented using a few numbers:

```text
+-----------------------------------+
|       REPOSITORY SNAPSHOT         |
+-----------------------------------+
| Source Files       : 1,092       |
| Lines of Code      : 386,608     |
| Commits            : 33,997      |
| Contributors       : 3,528      |
| Code Additions     : 3,747,733   |
| Code Deletions     : 3,170,166   |
+-----------------------------------+
```

This idea shows how large amounts of raw repository information can be converted into a small, understandable summary.

---

# 13. Project Structure

```text
CSET456Lab/
│
├── lab1/
│
└── lab2/
    │
    ├── src/
    │   └── mine_repositories.py
    │
    ├── data/
    │   ├── source_code_dataset.csv
    │   ├── commit_history_dataset.csv
    │   ├── cleaned_source_code_dataset.csv
    │   ├── cleaned_commit_history_dataset.csv
    │   └── merged_repository_dataset.csv
    │
    ├── output/
    │   ├── source_code_statistics.json
    │   ├── commit_history_statistics.json
    │   └── merged_dataset_statistics.json
    │
    └── README.md
```

---

# 14. My Learning

This lab helped me understand repository mining in a more practical way.

Before this lab, I mainly thought of a Git repository as a place where source code and commits are stored. During this lab, I learned that a repository can also be treated as a source of structured data.

I learned how information such as:

* source files
* programming languages
* lines of code
* commits
* contributors
* additions
* deletions

can be extracted and converted into datasets.

I also learned that data cleaning is not always about removing records. It can also involve checking whether the collected information is valid, complete and relevant.

Another useful learning was working with Git history programmatically. Instead of manually checking thousands of commits, the mining program can collect the information automatically.

Overall, this lab gave me a better understanding of how software repositories can be analyzed as datasets and how repository mining can be useful for software engineering analysis.

---

# 15. Conclusion

In this lab, five open-source repositories were mined to create three different datasets.

The first dataset describes the source code, the second describes the Git commit history, and the third combines important information from both at repository level.

The datasets were cleaned, analyzed and summarized using JSON statistics files.

The project demonstrates that repository mining can convert large amounts of software development information into structured data that can be used for codebase analysis, development activity analysis, contributor analysis and repository comparison.

The work can be extended in the future by creating visual dashboards and time-based graphs to show how repositories change over their development history.
