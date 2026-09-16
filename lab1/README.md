# LAB-1: Mining and Profiling a Software Repository

## Objective

The objective of this lab is to analyze an open-source software repository using Python and Git history.

The main goal is to understand how a software repository can be treated as a source of useful software engineering data. The analysis covers both the current structure of the repository and its development history.

---

## Repository Selected

For this lab, I selected the Flask repository from GitHub.

**Repository:** Flask
**Source:** https://github.com/pallets/flask

Flask is a lightweight Python web framework. It was a good choice for this lab because it has a real-world codebase with source files, documentation, multiple file types, and a long Git history.

---

## Tools Used

The following tools were used during the analysis:

* **Python** - Used to write the repository analysis program.
* **PyDriller** - Used to mine and analyze Git commit history.
* **Git** - Used to clone the repository and manage the lab work.
* **CSV** - Used to store file-level and monthly Git datasets.
* **JSON** - Used to store the overall repository statistics.
* **VS Code** - Used to write and organize the analysis code and documentation.

### Association of Tools with the Project

| Tool      | Association with the Project                                        |
| --------- | ------------------------------------------------------------------- |
| Python    | Main programming language used to implement the repository analyzer |
| PyDriller | Used to analyze Git commits and repository history                  |
| Git       | Used to obtain the repository and manage version history            |
| CSV       | Used to store structured file and monthly metrics                   |
| JSON      | Used to store summarized repository statistics                      |
| VS Code   | Used for development, testing, and documentation                    |

---

# 1. Repository Analysis

First, the Flask repository was scanned file by file.

The program identified source-code files and collected information such as:

* File path
* Programming language
* File extension
* Lines of Code (LOC)
* File size
* File-type distribution

This information was then stored as structured data in CSV and JSON files.

### Source-Code Identification

The program used file extensions to identify the programming language.

For example:

* `.py` → Python
* `.html` → HTML
* `.css` → CSS
* `.sh` → Shell

The repository's `.git` directory was not treated as project source code because it contains Git's internal metadata and version-control information.

---

## Repository Inventory

After scanning the Flask repository, the following information was collected:

| Metric       |  Value |
| ------------ | -----: |
| Total Files  |    236 |
| Source Files |    106 |
| Directories  |     51 |
| Total LOC    | 14,528 |

### Programming Languages

| Language | Number of Files |
| -------- | --------------: |
| Python   |              83 |
| HTML     |              20 |
| CSS      |               2 |
| Shell    |               1 |

The results show that Python is the main language used in the repository. This is expected because Flask is a Python web framework.

# 2. File-Level Metrics

The next part of the analysis focused on individual source files.

For each source file, the program collected:

| Field        | Description                                |
| ------------ | ------------------------------------------ |
| `file_path`  | Location of the file inside the repository |
| `language`   | Programming language used                  |
| `extension`  | File extension                             |
| `loc`        | Number of non-empty lines of code          |
| `size_bytes` | File size in bytes                         |

These metrics provide a basic profile of the source code and make it possible to compare files based on their size and complexity-related characteristics.

### Example of File-Level Data

A source-code dataset can be represented in the following form:

```text
repository,file_path,language,extension,loc,size_bytes
Flask,flask/app.py,Python,.py,...,...
Flask,flask/helpers.py,Python,.py,...,...
```

Each row represents one source file.

---

# 3. Git History Analysis

After analyzing the current repository structure, the development history of Flask was analyzed.

PyDriller was used to examine commits and extract information from the Git history.

The analysis included:

* Total number of commits
* Number of contributors
* Most active contributor
* Frequently changed files
* Files changed per commit
* Lines added
* Lines deleted
* Monthly commit activity

### Repository Git Statistics

The Flask repository contained:

| Metric                           | Value |
| -------------------------------- | ----: |
| Total Commits                    | 5,556 |
| Contributors                     |   858 |
| Average Files Changed per Commit |  1.67 |
| Average Lines Added per Commit   | 21.43 |
| Average Lines Deleted per Commit | 14.60 |

These values provide an overview of the development activity present in the repository history.

---

## Most Active Contributor

The analysis also identified contributors based on their number of commits.

The most active contributor in the analyzed history was:

**David Lord — 1,855 commits**

This metric shows how commit activity can be analyzed at the contributor level.

It does not necessarily represent the total amount of code written by a contributor because a commit can contain different amounts of work.

---

## Frequently Changed Files

The analysis also identified files that appeared frequently in commit changes.

Some of the frequently changed files were:

| File                  | Number of Changes |
| --------------------- | ----------------: |
| `flask\app.py`        |               354 |
| `CHANGES.rst`         |               342 |
| `CHANGES`             |               317 |
| `flask\helpers.py`    |               204 |
| `docs\quickstart.rst` |               185 |

This information can help identify files that have received significant development activity over the repository's history.

---

# 4. Monthly Git Metrics

Git history was also organized by month to understand development activity over time.

The monthly dataset contains information related to:

* Month
* Number of commits
* Files changed
* Lines added
* Lines deleted

This allows the repository history to be viewed as a time-based dataset instead of only as individual commits.

For example, monthly commit data can help answer questions such as:

* Which months had higher development activity?
* How many commits were made during a particular period?
* Were more lines added or deleted during certain periods?
* How did development activity change over time?

---

# 5. Data Generated

The analysis generated structured output files containing the mined information.

### CSV Outputs

The CSV files contain structured tabular data that can be opened and analyzed using spreadsheet software or Python.

Examples include:

* `file_metrics.csv`
* `monthly_git_metrics.csv`

### JSON Output

The repository-level statistics were stored in:

* `repository_statistics.json`

JSON was useful for storing summarized metrics in a structured format that can also be consumed by other programs.

---

# 6. Repository Statistics

The JSON statistics provide a summarized view of the repository.

The statistics include information such as:

* Total files
* Source files
* Directories
* Total lines of code
* Language distribution
* Total commits
* Contributors
* Most active contributor
* Frequently changed files
* Average files changed
* Average additions
* Average deletions

This makes it easier to use the mining results in another application or visualization without processing the complete datasets again.

---

# 7. Source-Code Analysis vs Repository Mining

An important concept learned in this lab is the difference between source-code analysis and repository mining.

### Source-Code Analysis

Source-code analysis focuses on the code currently present in the repository.

Examples:

* Number of source files
* Programming languages
* Lines of code
* File size
* File structure

### Repository Mining

Repository mining includes the development history and activity around the code.

Examples:

* Commits
* Contributors
* Files changed
* Lines added
* Lines deleted
* Monthly development activity

---

# 8. Project Structure

The Lab 1 project was organized as follows:

```text
lab1/
├── src/
│   └── repository_analyzer.py
│
├── data/
│   ├── file_metrics.csv
│   └── monthly_git_metrics.csv
│
├── output/
│   └── repository_statistics.json
│
└── README.md
```

The source code is kept separate from generated datasets and output statistics to make the project easier to understand and maintain.

---

# 9. Learning Outcomes

This lab helped me understand how a real-world Git repository can be treated as structured software engineering data.

The main things I learned were:

* How to scan a repository programmatically using Python.
* How to identify files and programming languages using file extensions.
* How to calculate basic source-code metrics such as LOC and file size.
* How Git stores development history through commits.
* How PyDriller can be used to analyze Git history.
* How to extract contributor and commit information.
* How to organize extracted information into CSV and JSON datasets.
* How source-code information and development-history information provide different views of a software project.
* How repository mining can be useful for software engineering research and analysis.

---

# 10. Conclusion

This lab provided a practical introduction to mining and profiling a real-world software repository.

The Flask repository was analyzed using Python and PyDriller. Repository-level and file-level information was collected, Git history was mined, and the results were converted into structured CSV and JSON datasets.

The analysis covered the current structure of the repository as well as its development history. The repository contained **236 files, 106 identified source files, 14,528 non-empty lines of code, 5,556 commits, and 858 contributors** in the analyzed data.

The lab also helped me understand the difference between source-code analysis and repository mining. Source-code analysis focuses on what is present in the codebase, while repository mining helps us understand the development activity behind it.

Overall, this lab showed that a Git repository is much more than a place to store code. It can also be treated as a valuable source of software engineering data that can be analyzed, visualized, and used for further research.
