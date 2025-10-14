# src/scenario_input.py
from typing import List, Optional
from demo_dataset import get_demo_scenarios

def get_scenarios_from_user(prompt_text: str = "Enter scenario (or blank to skip): ") -> Optional[str]:
    """
    Simple CLI input helper — returns single scenario string or None if empty.
    """
    try:
        s = input(prompt_text).strip()
        return s if s else None
    except KeyboardInterrupt:
        return None

def get_demo_batch(csv_file: str = None) -> List[str]:
    """
    Return a list of demo scenarios. If csv_file is None, uses default demo file.
    """
    if csv_file:
        return get_demo_scenarios(csv_file)
    return get_demo_scenarios()
