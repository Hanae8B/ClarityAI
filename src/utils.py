"""
utils.py – Utility functions for ClarityAI
Includes CSV loading, keyword parsing, and scenario loading.
"""

import csv
from config import DEMO_KEYWORDS_CSV

# Load keywords
def load_demo_keywords(csv_path=DEMO_KEYWORDS_CSV) -> dict:
    """
    Load keywords from CSV.
    Expected format:
        category,keyword1,keyword2,...
    Returns:
        { category1: [keyword1, keyword2, ...], ... }
    """
    keywords_dict = {}
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)  # skip header
            for row in reader:
                if not row:
                    continue
                category = row[0].strip()
                keywords = [kw.strip() for kw in row[1:] if kw.strip()]
                if category and keywords:
                    keywords_dict[category] = keywords
    except Exception as e:
        print(f"⚠️ Failed to load keywords from {csv_path}: {e}")
    return keywords_dict

# Load sample scenarios
def load_sample_scenarios(csv_path) -> list:
    """
    Load scenario text from CSV.
    Expected format:
        Scenario
        <scenario text>
    Returns a list of scenario strings.
    """
    scenarios = []
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)  # skip header
            for row in reader:
                if row:
                    scenarios.append(row[0].strip())
    except Exception as e:
        print(f"⚠️ Failed to load scenarios from {csv_path}: {e}")
    return scenarios
