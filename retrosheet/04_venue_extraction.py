import csv

import requests

URL = "https://statsapi.mlb.com/api/v1/venues?hydrate=xrefId"

OUTPUT_FILE = "venues.csv"
COLUMNS = ["key_mlbam", "key_retro", "venue_name"]


def fetch_venue_xref_lookup():
    resp = requests.get(URL)
    resp.raise_for_status()
    data = resp.json()

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as out_csv:
        writer = csv.DictWriter(out_csv, fieldnames=COLUMNS)
        writer.writeheader()

        for v in data.get("venues", []):
            mlbam_venue_id = v.get("id")
            venue_name = v.get("name")
            for xref in v.get("xrefIds", []):
                if xref["xrefType"] != "retrosheet":
                    continue
                writer.writerow(
                    {
                        "key_mlbam": mlbam_venue_id,
                        "key_retro": xref["xrefId"],
                        "venue_name": venue_name,
                    }
                )


print(f"✅ Combined file written to: {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_venue_xref_lookup()
