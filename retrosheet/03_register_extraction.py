import csv
import glob
import os

# git clone git@github.com:chadwickbureau/register.git

# Directory containing your people-*.csv files
INPUT_DIR = "data"
OUTPUT_FILE = "people.csv"

# Columns to extract
COLUMNS = ["key_mlbam", "key_retro", "name_last", "name_first"]

# Find all CSV files matching pattern people-0.csv ... people-z.csv
input_files = sorted(glob.glob(os.path.join(INPUT_DIR, "people-[0-9a-z].csv")))

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as out_csv:
    writer = csv.DictWriter(out_csv, fieldnames=COLUMNS)
    writer.writeheader()

    for file in input_files:
        with open(file, newline="", encoding="utf-8") as in_csv:
            reader = csv.DictReader(in_csv)
            for i, row in enumerate(reader, start=2):  # start=2 since header is line 1
                key_mlbam = row.get("key_mlbam", "").strip()
                key_retro = row.get("key_retro", "").strip()
                if not key_mlbam or not key_retro:
                    continue
                writer.writerow(
                    {
                        "key_mlbam": key_mlbam,
                        "key_retro": key_retro,
                        "name_last": row.get("name_last", "").strip(),
                        "name_first": row.get("name_first", "").strip(),
                    }
                )

print(f"✅ Combined file written to: {OUTPUT_FILE}")
