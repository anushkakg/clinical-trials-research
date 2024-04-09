import httpx
import pandas as pd
import tqdm

API_URL = "https://clinicaltrials.gov/api/v2/studies?pageSize=1000"

response_json = httpx.get(API_URL).json()
df = pd.json_normalize(response_json.get("studies"))

for _ in tqdm.trange(492):
    try:
        next_page_token = response_json.get("nextPageToken")
        response_json = httpx.get(API_URL + f"&pageToken={next_page_token}").json()
        df = pd.concat(
            [df, pd.json_normalize(response_json["studies"])], ignore_index=True
        )
    except Exception as e:
        print(f"Encountered erorr {e}.")
        break

print("Finished downloading!")
df.to_csv("./fields.csv")
