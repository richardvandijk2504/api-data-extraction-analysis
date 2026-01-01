import requests
import json
from pathlib import Path
from time import sleep

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(exist_ok=True)

#API-Extraction parameters
BASE_URL = "https://api.openalex.org/works"
PAGE_STEP = 200
MAX = 300_000

def get_Data(RAW_DIR, BASE_URL, MAX, PAGE_STEP):
    """
    Connects to the API Endpoint (OpenAlex) and requests data which runs 
    to MAX_RECORDS in steps of PER_PAGE records to create a .json file in RAW_DIR 
    and save raw data to it. Retuns raw data json file.
    """
    cursor = "*"
    total = 0
    page_num = 1

    while total < MAX:
        params = {"per-page": PAGE_STEP, "cursor": cursor}
        r = requests.get(BASE_URL, params=params)
        if r.status_code != 200:
            print(f"Error {r.status_code}")
            break
        #JSON-ify request r to data and store to results
        data = r.json()
        results = data.get("results", [])
        if not results:
            break

        with open(RAW_DIR / f"page_{page_num:04d}.json", "w") as j_file:
            json.dump(results, j_file)

        total += len(results)
        print(f"Page {page_num}, total records: {total}")

        cursor = data.get("meta", {}).get("next_cursor")
        if not cursor:
            break

        page_num += 1

if __name__ == "__main__":
    get_Data(RAW_DIR, BASE_URL, MAX, PAGE_STEP)
