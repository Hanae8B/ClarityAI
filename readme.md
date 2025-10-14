# ClarityAI

ClarityAI is a tool for analyzing scenarios using semantic similarity and causal relationships. It identifies relevant categories in a scenario and provides possible causal explanations.

---

## Features

- Analyze scenarios in **CLI**, **GUI**, or **batch mode**  
- Detect top relevant categories for a scenario  
- Provide causal explanations for category interactions  
- Visualize top categories as a bar chart with causal categories highlighted  

---

## Installation

1. Ensure Python 3.11+ is installed  
2. Clone or copy the project to a local directory, for example:  

C:\ClarityAI

3. Install dependencies:  

\`\`\`bat
pip install -r C:\ClarityAI\src\requirements.txt
\`\`\`

4. Download the spaCy model:

\`\`\`bat
python -m spacy download en_core_web_md
\`\`\`

---

## Running ClarityAI

Run the main script using the provided batch file:

\`\`\`bat
C:\ClarityAI\run_clarity.bat
\`\`\`

You will be prompted to select a mode:

- [1] CLI – Enter scenarios interactively
- [2] GUI – Enter scenarios and see textual and graphical output
- [3] Batch – Process scenarios from sample_scenarios.csv

---

## File Structure

C:\ClarityAI
│
├─ src
│ ├─ main.py
│ ├─ gui_clarity.py
│ ├─ explanation_engine.py
│ ├─ visualization.py
│ ├─ utils.py
│ ├─ config.py
│ └─ requirements.txt
│
├─ data
│ ├─ demo_keywords.csv
│ └─ sample_scenarios.csv
│
└─ run_clarity.bat


---

## Author
Anna Baniakina
