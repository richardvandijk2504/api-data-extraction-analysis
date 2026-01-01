from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent.resolve()

CLEAN_DIR = PROJECT_ROOT / "data" / "cleaned"
FINAL_DIR = PROJECT_ROOT / "data" / "final"
FINAL_DIR.mkdir(parents=True, exist_ok=True)

def extract_feat(CLEAN_DIR, FINAL_DIR):
    """
    Uses cleaned data and extracts the top 3 (concept_1, concept_2,
    concept_3) and total nr of concepts per paper (n_concepts). 
    Returns output path for the finalized data.
    """
    df = pd.read_csv(CLEAN_DIR / "API_data_cleaned.csv")

    df["publication_year"] = pd.to_numeric(df["publication_year"], errors="coerce")
    df["publication_date"] = pd.to_datetime(df["publication_date"], errors="coerce")

    concepts_split = df["concepts"].fillna("").apply(lambda x: x.split(",") if x else [])

    top_n = 3
    for i in range(top_n):
        df[f"concept_{i+1}"] = concepts_split.apply(
            lambda lst: lst[i] if len(lst) > i else None
        )

    df["n_concepts"] = concepts_split.apply(len)

    output = FINAL_DIR / "API_data_final.csv"
    df.to_csv(output, index=False)
    print(f"Saved analysis-ready data: {output} ({len(df)} rows)")

if __name__ == "__main__":
    extract_feat(CLEAN_DIR, FINAL_DIR)
