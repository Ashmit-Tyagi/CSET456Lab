import os
import csv
import json
from collections import Counter
from pydriller import Repository


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

