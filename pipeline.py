import requests
import json
from pathlib import Path
from time import sleep

#Define git-dir path
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(exist_ok=True)

#Store API-Extraction parameters
BASE_URL = "https://api.openalex.org/works"
PER_PAGE = 200
MAX_RECORDS = 300_000

def fetch_API(RAW_DIR, BASE_URL, MAX_RECORDS, PER_PAGE):
  """connects to the API BASE_URL through a while loop which runs to MAX_RECORDS in steps of PER_PAGE.
     Creates JSON file in RAW_DIR and saves raw data to it
     
     Parameters:
    RAW_DIR (Path): directory to save raw JSON
    BASE_URL (str): API endpoint
    MAX_RECORDS (int): maximum total records to fetch
    PER_PAGE (int): number of records per API call
  """
  cursor = "*"
  total = 0
  page_num = 1

  while total < MAX_RECORDS:
      params = {"per-page": PER_PAGE, "cursor": cursor}
      r = requests.get(BASE_URL, params=params)
      if r.status_code != 200:
          print(f"Error {r.status_code}")
          break
      #JSON-ify request r to data and store to results
      data = r.json()
      results = data.get("results", [])
      if not results:
          break

      with open(RAW_DIR / f"page_{page_num:04d}.json", "w") as f:
          json.dump(results, f)

      total += len(results)
      print(f"Page {page_num}, total records: {total}")

      cursor = data.get("meta", {}).get("next_cursor")
      if not cursor:
          break

      page_num += 1
      sleep(1)  #Sleep to limit process rate 

if __name__ == "__main__":
    fetch_API(RAW_DIR, BASE_URL, MAX_RECORDS, PER_PAGE)
