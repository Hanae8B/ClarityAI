# src/demo_dataset.py
from typing import List
from config import SAMPLE_SCENARIOS_CSV
from utils import load_sample_scenarios

def get_demo_scenarios(csv_file: str = SAMPLE_SCENARIOS_CSV) -> List[str]:
    """
    Return a list of demo scenario strings loaded from CSV.
    """
    return load_sample_scenarios(csv_file)
