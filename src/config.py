"""
config.py – Configuration constants for ClarityAI
"""

import os

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# CSV file paths
DEMO_KEYWORDS_CSV = os.path.join(DATA_DIR, "demo_keywords.csv")
SAMPLE_SCENARIOS_CSV = os.path.join(DATA_DIR, "sample_scenarios.csv")
