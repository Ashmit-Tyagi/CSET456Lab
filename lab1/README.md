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

- **Python** - Used to write the repository analysis program.
- **PyDriller** - Used to mine and analyze Git commit history.
- **Git** - Used to clone the repository and manage the lab work.
- **CSV** - Used to store file-level and monthly Git datasets.
- **JSON** - Used to store the overall repository statistics.
- **VS Code** - Used to write and organize the analysis code and documentation.

---

## How the Analysis Works

The analysis was divided into two main parts.

### 1. Repository Analysis

First, the Flask repository was scanned file by file.

The program identified source-code files and collected information such as:

- File path
- Programming language
- File extension
- Lines of Code (LOC)
- File size
- File-type distribution

This information was then stored as structured data in CSV and JSON files.

### 2. Git History Analysis

After analyzing the repository files, PyDriller was used to go through the Git history of Flask.

The program collected information about:

- Total commits
- Contributors
- Most active contributor
- Frequently changed files
- Commits per month
- Files changed
- Lines added
- Lines deleted

This helped provide a historical view of how the project has developed over time.

---

## Repository Inventory

After scanning the Flask repository, the following information was collected:

| Metric | Value |
|---|---:|
| Total Files | 236 |
| Source Files | 106 |
| Directories | 51 |
| Total LOC | 14,528 |

### Programming Languages

| Language | Number of Files |
|---|---:|
| Python | 83 |
| HTML | 20 |
| CSS | 2 |
| Shell | 1 |

The results show that Python is the main language used in the repository. This is expected because Flask is a Python web framework.

### A Quick Look at the Numbers

The repository contains **236 files**, of which **106 were identified as source-code files**.

The total number of non-empty lines of code counted from the identified source files was **14,528**.

The remaining files include documentation, configuration files, and other project resources.

---

## File-Level Metrics

The next part of the analysis focused on individual source files.

For each source file, the program collected:

| Field | Description |
|---|---|
| `file_path` | Location of the file inside the repository |
| `language` | Programming language used |
| `extension` | File extension |
| `loc` | Number of non-empty lines of code |
| `size_bytes` | File size in bytes |

## Conclusion

This lab provided a practical introduction to mining and profiling a real-world software repository.

The Flask repository was analyzed using Python and PyDriller. Repository-level and file-level information was collected, Git history was mined, and the results were converted into structured CSV and JSON datasets.

The lab also helped me understand the difference between source-code analysis and repository mining. Source-code analysis focuses on what is present in the codebase, while repository mining helps us understand the development activity behind it.

Overall, this lab showed that a Git repository is much more than a place to store code. It can also be treated as a valuable source of software engineering data that can be analyzed, visualized, and used for further research.