# Global Video Game Sales — Data Visualization Final Project

## Overview
Analysis of 16,598 video game titles (1980–2016) exploring platform dominance, sales trends, regional genre preferences, publisher performance, and console lifecycle patterns — through 10 analytical questions, each answered with a Plotly visualization.

## Dataset
- **Source:** [Kaggle — Video Game Sales](https://www.kaggle.com/datasets/gregorut/videogamesales)
- **File:** `vgsales.csv` (included in this repo)
- Fields: Name, Platform, Year, Genre, Publisher, NA/EU/JP/Other/Global Sales (millions of units)

## Files in this repo
| File | Description |
|---|---|
| `vgsales_analysis.ipynb` | Full analysis notebook — 10 questions, code, Plotly charts |
| `vgsales_analysis.html` | HTML export of the notebook (charts included) |
| `vgsales_presentation.pdf` | Slide deck summarizing findings |
| `app.py` | Streamlit dashboard source code |
| `vgsales.csv` | Dataset used |

## Live Dashboard
🔗 https://wve3bazbsyzgbcbysaagy3.streamlit.app

## Key Findings
1. Sales are concentrated, not spread evenly — the PS2 alone accounts for ~1.2B units.
2. Global sales peaked in 2008, then declined (coinciding with digital distribution's rise).
3. Regional taste diverges: Japan favors RPGs; NA/EU favor Action and Sports.
4. Nintendo leads total publisher sales, but genre leadership is specialized.
5. Console lifecycles follow a boom-then-decline pattern (e.g. the Wii).

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
