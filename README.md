API Data Extraction and Cleaning Pipeline
========================================

Project Overview
----------------
This project demonstrates a complete pipeline for extracting, cleaning, and preparing bibliometric data
from the OpenAlex API (or after simple-modification any similar API Endpoint). The pipeline handles pagination, flattens nested JSON data, normalizes fields,
and produces a clean CSV suitable for exploratory data analysis (EDA) or machine learning tasks.

Folder Structure
----------------
data/
    raw/        # Raw JSON pages fetched from the OpenAlex API
    cleaned/    # Flattened, cleaned CSV from raw data
    final/      # Analysis-ready CSV with extracted features (top concepts, counts, dates)

utils/
    pipeline.py # Script to fetch data from OpenAlex API with pagination
    clean.py    # Script to flatten and clean raw JSON into a single CSV
    extract.py  # Script to generate analysis-ready dataset with feature extraction

requirements.txt
    List of Python packages required: requests, pandas, numpy, matplotlib, pyarrow, tqdm, pytest

Usage Instructions
------------------
It is generally recommended to create a virtual environment to 
ensure a consistent package setup by opening a bash or powershell terminal
and running the following lines:
  
  python -m venv venv
  venv/Scripts/activate (Windows)
  source venv/bin/activate (macOS/Linux)

After this the tutorial below can be followed in the same manner.


1. Install dependencies:
    pip install -r requirements.txt

2. Fetch raw data from OpenAlex API:
    python utils/pipeline.py
    - Fetches multiple pages of works using pagination
    - Saves each page as `page_XXXX.json` in `data/raw/`

3. Clean raw JSON into a single CSV:
    python utils/clean.py
    - Flattens nested dictionaries (concepts)
    - Drops duplicate works
    - Saves `API_data_cleaned.csv` in `data/cleaned/`

4. Extract features and prepare analysis-ready CSV:
    python utils/extract.py
    - Splits top N concepts into separate columns (set top_n in extract.py)
    - Counts number of concepts per paper
    - Converts publication_year to numeric and publication_date to datetime to ensure proper types
    - Saves `API_data_final.csv` in `data/final/`

Key Features
------------
- Handles large datasets with API pagination
- Cleans and flattens nested JSON structures
- Produces reusable, analysis-ready CSV files
- Feature extraction for EDA or ML pipelines
- Fully reproducible and modular pipeline
- Counts and visualizes the Top 10 most frequent concepts
- Generates publication trends per year (total and per top concept)
- Jupyter notebooks for visual analysis of concepts and publications per year

Potential Extensions
--------------------
- Include concept scores for weighted analysis
- Extend visualization notebook(s)

Contact / Author
----------------
Richard van Dijk
Email: [richardvandijk2504@gmail.com]
Portfolio: [https://github.com/richardvandijk2504]
