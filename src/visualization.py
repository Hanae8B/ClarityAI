"""
visualization.py – Graphical displays for ClarityAI
Enhanced version: highlights causal categories in the bar chart.
"""

import matplotlib.pyplot as plt

def plot_categories(result):
    """
    Plot top categories with their scores as a horizontal bar chart.
    Categories involved in causal explanations are highlighted.
    """
    if not result.get("top_categories"):
        print("⚠️ No categories to plot.")
        return

    categories = [cat for cat, score in result["top_categories"]]
    scores = [score for cat, score in result["top_categories"]]

    # Determine which categories are part of causal explanations
    causal_cats = set()
    for exp in result.get("causal_explanations", []):
        pair = exp.split(":")[0]  # "cat1 + cat2"
        for cat in pair.split(" + "):
            causal_cats.add(cat.strip())

    colors = ['orange' if cat in causal_cats else 'skyblue' for cat in categories]

    plt.figure(figsize=(8, 4))
    plt.barh(categories, scores, color=colors)
    plt.xlabel("Similarity Score")
    plt.xlim(0, 1)
    plt.title("Top Categories (orange = causal pair)")
    plt.gca().invert_yaxis()  # highest score on top
    plt.tight_layout()
    plt.show()

def display_causal_explanations(result):
    """
    Display causal explanations in a simple list format.
    """
    if not result.get("causal_explanations"):
        print("⚠️ No causal explanations found.")
        return

    print("\nCausal Explanations:")
    for exp in result["causal_explanations"]:
        print(f" - {exp}")
