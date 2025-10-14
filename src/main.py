"""
main.py – ClarityAI entry point with GUI, CLI, batch, and visualization support
"""

import os
from explanation_engine import ExplanationEngine
from utils import load_sample_scenarios
from config import SAMPLE_SCENARIOS_CSV
from visualization import plot_categories, display_causal_explanations

# Import GUI launcher
try:
    from gui_clarity import launch_gui
    GUI_AVAILABLE = True
except Exception:
    GUI_AVAILABLE = False

# Print
def print_explanation(result):
    print("\n--- ClarityAI Explanation ---")
    print(f"Scenario:\n{result['scenario']}\n")
    print("Top categories (category: score):")
    if result["top_categories"]:
        for cat, score in result["top_categories"]:
            print(f" - {cat}: {score:.3f}")
    else:
        print(" - (no relevant categories detected)")
    print("\nCausal explanations:")
    if result["causal_explanations"]:
        for exp in result["causal_explanations"]:
            print(f" - {exp}")
    else:
        print(" - (none found)")
    print(f"\nEngine model: {result['model']}")
    print("--- End Explanation ---\n")

# Interactive CLI mode
def interactive_mode(engine):
    print("🧠 ClarityAI Interactive Mode")
    print("Type a scenario, or 'exit' to quit.\n")
    while True:
        scenario = input("> ").strip()
        if scenario.lower() in {"exit", "quit"}:
            print("Exiting ClarityAI. Goodbye!")
            break
        if not scenario:
            continue
        result = engine.analyze_scenario(scenario)
        print_explanation(result)
        plot_categories(result)
        display_causal_explanations(result)

# Batch mode
def batch_mode(engine):
    print(f"📂 Loading sample scenarios from: {SAMPLE_SCENARIOS_CSV}")
    scenarios = load_sample_scenarios(SAMPLE_SCENARIOS_CSV)
    if not scenarios:
        print("⚠️ No scenarios found in dataset.")
        return
    print(f"Processing {len(scenarios)} scenarios...\n")
    for idx, scenario in enumerate(scenarios, start=1):
        print(f"▶ Scenario {idx}/{len(scenarios)}")
        result = engine.analyze_scenario(scenario)
        print_explanation(result)
        plot_categories(result)
        display_causal_explanations(result)

# Main
def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # project root
    engine = ExplanationEngine()

    # Ask user for mode
    mode = input("Select mode: [1] CLI, [2] GUI, [3] Batch: ").strip()
    if mode == "2" and GUI_AVAILABLE:
        launch_gui(engine)
    elif mode == "3":
        batch_mode(engine)
    else:
        interactive_mode(engine)

if __name__ == "__main__":
    main()
