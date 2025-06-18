#!/usr/bin/env python3
"""
Populate the `img_url` column with a 400-pixel thumbnail URL for each
scientist, batching the Q-IDs so every SPARQL request is small and POST-ed.
"""

import time, textwrap, requests, pandas as pd, urllib.parse

#!/usr/bin/env python3
"""
Populate the `img_url` column with a 400-pixel thumbnail URL for each
scientist, batching the Q-IDs so every SPARQL request is small and POST-ed.
"""

import time, textwrap, requests, pandas as pd, urllib.parse

CSV_FILE = "scientists.csv"   # in-place update
BATCH    = 50                                # Q-IDs per request
ENDPOINT = "https://query.wikidata.org/sparql"
HEADERS  = {
    "User-Agent": "scientist-timeline/0.1 (https://github.com/YOUR_REPO)",
    "Accept": "application/sparql-results+json"
}

df = pd.read_csv(CSV_FILE)
if "wd_id" not in df.columns:
    raise ValueError("Need a 'wd_id' column (e.g. Q937)")

needs_pic = df["img_url"].isna() if "img_url" in df.columns else [True] * len(df)
qid_queue = df.loc[needs_pic, "wd_id"].tolist()
print(f"{len(qid_queue)} scientists without img_url – fetching…")

pictures = {}
for i in range(0, len(qid_queue), BATCH):
    qids = qid_queue[i:i+BATCH]
    values = " ".join(f"wd:{q}" for q in qids)

    # ***  No regex, just return ?orig  ***
    sparql = textwrap.dedent(f"""
        SELECT ?item ?orig WHERE {{
          VALUES ?item {{ {values} }}
          ?item wdt:P18 ?orig .
        }}
    """)

    r = requests.post(ENDPOINT,
                      data={"query": sparql, "format": "json"},
                      headers=HEADERS, timeout=60)
    r.raise_for_status()

    for b in r.json()["results"]["bindings"]:
        qid  = b["item"]["value"].split("/")[-1]          # Q12345
        orig = b["orig"]["value"]                         # a Commons FilePath URL
        # build a light 400-px thumbnail: Special:FilePath […]?width=400
        pictures[qid] = orig + "?width=400"

    time.sleep(1.1)                                      # WDQS rate-limit

print(f"✓ got {len(pictures)} thumbnails")

# merge back into the DataFrame
df["img_url"] = df.apply(
    lambda row: pictures.get(row["wd_id"], row.get("img_url", None)),
    axis=1
)
df.to_csv(CSV_FILE, index=False)
print(f"→ updated {CSV_FILE} with img_url column")

