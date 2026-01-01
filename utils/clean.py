import json
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent.resolve()

RAW_DIR = PROJECT_ROOT / "data" / "raw"
CLEAN_DIR = PROJECT_ROOT / "data" / "cleaned"
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

def flatten_data(page):
    """
    Takes list of dictionaries, page, and flattens the concept 
    dictionary (ordered by OpenAlex concept score) and aggregates
    it with flat raw data, returning a flat list of dictionaries. 
    """
    
    return {
        "id": page.get("id"),
        "title": page.get("title"),
        "doi": page.get("doi"),
        "type": page.get("type"),
        "publication_year": page.get("publication_year"),
        "publication_date": page.get("publication_date"),
        #Order concepts by OpenAlex concept score
        "concepts": ",".join(
            concept.get("display_name", "")
            for concept in sorted(page.get("concepts", []),
                            key=lambda x: x.get("score", 0),
                            reverse=True)
        )
    }

def clean_raw_data():
    """
    Runs for loop over all .json page files in data/raw, applies the flatten_data 
    function and creates a cleaned data file (data/cleaned/API_data_cleaned.csv).
    Used as Main Function, requires no input.
    """
    rows = []

    for file in RAW_DIR.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for page in data:
            rows.append(flatten_data(page))

    df = pd.DataFrame(rows)
    df.drop_duplicates(subset="id", inplace=True)

    output = CLEAN_DIR / "API_data_cleaned.csv"
    df.to_csv(output, index=False)
    print(f"Saved cleaned data: {output} ({len(df)} rows)")

if __name__ == "__main__":
    clean_raw_data()
