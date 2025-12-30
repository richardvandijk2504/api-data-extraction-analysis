from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent.resolve()

CLEAN_DIR = PROJECT_ROOT / "data" / "cleaned"
FINAL_DIR = PROJECT_ROOT / "data" / "final"
FINAL_DIR.mkdir(parents=True, exist_ok=True)

def extract_features(CLEAN_DIR, FINAL_DIR):
    """
    Function that uses the cleaned data ensure publication years and dates are proper types and extract
    the top 3 (concept_1, concept_2, concept_3) and total nr of concepts per paper (n_concepts).
    
    Takes as input the cleaned data path, CLEAN_DIR, 
    and the output path FINAL_DIR for the finalized data it outputs.
    """
    df = pd.read_csv(CLEAN_DIR / "API_data_cleaned.csv")

    #Ensure publication types are correct
    df["publication_year"] = pd.to_numeric(df["publication_year"], errors="coerce")
    df["publication_date"] = pd.to_datetime(df["publication_date"], errors="coerce")

    #Split concepts
    concepts_split = df["concepts"].fillna("").apply(lambda x: x.split(",") if x else [])

    #Get top N concepts
    top_n = 3
    for i in range(top_n):
        df[f"concept_{i+1}"] = concepts_split.apply(
            lambda lst: lst[i] if len(lst) > i else None
        )

    #Count nr of concepts
    df["n_concepts"] = concepts_split.apply(len)

    output = FINAL_DIR / "API_data_final.csv"
    df.to_csv(output, index=False)
    print(f"Saved analysis-ready data → {output} ({len(df)} rows)")

if __name__ == "__main__":
    extract_features(CLEAN_DIR, FINAL_DIR)

