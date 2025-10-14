import tkinter as tk
from tkinter import ttk, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def launch_gui(engine):
    window = tk.Tk()
    window.title("ClarityAI - Scenario Analyzer")
    window.geometry("900x700")  # initial size
    window.minsize(800, 600)    # minimum size
    window.columnconfigure(0, weight=1)
    window.rowconfigure(3, weight=1)  # make output area expandable

    # Header
    header = ttk.Label(window, text="ClarityAI Scenario Analyzer", font=("Arial", 16, "bold"))
    header.grid(row=0, column=0, pady=10)

    # Scenario input
    scenario_frame = ttk.Frame(window)
    scenario_frame.grid(row=1, column=0, padx=10, sticky="ew")
    scenario_frame.columnconfigure(1, weight=1)

    scenario_label = ttk.Label(scenario_frame, text="Enter scenario:")
    scenario_label.grid(row=0, column=0, padx=(0,5), sticky="w")

    scenario_var = tk.StringVar()
    scenario_entry = ttk.Entry(scenario_frame, textvariable=scenario_var)
    scenario_entry.grid(row=0, column=1, sticky="ew")

    # Analyze button
    analyze_btn = ttk.Button(window, text="Analyze Scenario")
    analyze_btn.grid(row=2, column=0, pady=5)

    # Output area (scrollable)
    output_area = scrolledtext.ScrolledText(window, wrap=tk.WORD)
    output_area.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

    # Figure area for bar chart
    fig, ax = plt.subplots(figsize=(6,3))
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

    # Analyze function
    def analyze_scenario(event=None):
        scenario_text = scenario_var.get().strip()
        if not scenario_text:
            output_area.delete(1.0, tk.END)
            output_area.insert(tk.END, "⚠️ Please enter a scenario.\n")
            return

        result = engine.analyze_scenario(scenario_text)

        # Clear previous outputs
        output_area.delete(1.0, tk.END)
        ax.clear()

        # Text output
        output_area.insert(tk.END, f"--- ClarityAI Explanation ---\n")
        output_area.insert(tk.END, f"Scenario:\n{result['scenario']}\n\n")
        output_area.insert(tk.END, "Top categories (category: score):\n")
        if result["top_categories"]:
            categories = []
            scores = []
            for cat, score in result["top_categories"]:
                output_area.insert(tk.END, f" - {cat}: {score:.3f}\n")
                categories.append(cat)
                scores.append(score)
            # Plot with causal highlighting
            causal_cats = set()
            for exp in result.get("causal_explanations", []):
                pair = exp.split(":")[0]
                for cat in pair.split(" + "):
                    causal_cats.add(cat.strip())
            colors = ['orange' if cat in causal_cats else 'skyblue' for cat in categories]
            ax.barh(categories, scores, color=colors)
            ax.set_xlabel("Similarity Score")
            ax.set_xlim(0,1)
            ax.invert_yaxis()
            ax.set_title("Top Categories (orange = causal pair)")
            canvas.draw()
        else:
            output_area.insert(tk.END, " - (no relevant categories detected)\n")

        # Causal explanations
        output_area.insert(tk.END, "\nCausal explanations:\n")
        if result["causal_explanations"]:
            for exp in result["causal_explanations"]:
                output_area.insert(tk.END, f" - {exp}\n")
        else:
            output_area.insert(tk.END, " - (none found)\n")

        output_area.insert(tk.END, f"\nEngine model: {result['model']}\n")
        output_area.insert(tk.END, "--- End Explanation ---\n")

    # Bind analyze function
    analyze_btn.config(command=analyze_scenario)
    scenario_entry.bind("<Return>", analyze_scenario)

    window.mainloop()
