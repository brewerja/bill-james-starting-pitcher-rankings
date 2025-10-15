from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup


def get_pitcher_ratings(month: int, day: int, year: int) -> list[dict[str, str]]:
    """Fetch and parse pitcher ratings for a given date from Baseball Musings."""

    # Build the query string for rankdate (e.g., 10/07/2025)
    params = {"rankdate": f"{month:02d}/{day:02d}/{year}"}
    url = (
        f"https://www.baseballmusings.com/cgi-bin/PitcherRatings.py?{urlencode(params)}"
    )

    print(f"Fetching {url}")
    response = requests.get(url)
    response.raise_for_status()  # raise an error if the request failed

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the ratings table (the page typically has a <table> with headers)
    table = soup.find("table", class_="dbd")
    if not table:
        raise ValueError("Could not find a ratings table on the page.")

    # Extract table headers
    headers = [th.get_text(strip=True) for th in table.find_all("th")]

    # Extract table rows
    rows = []
    for tr in table.find_all("tr")[1:]:  # skip header row
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cells:
            rows.append(dict(zip(headers, cells)))

    return rows


if __name__ == "__main__":
    for i in range(7, 1, -1):
        ratings = get_pitcher_ratings(10, i, 2025)
        print(f"Found {len(ratings)} pitchers.")
        for r in ratings[:10]:  # show first 5
            print(r)
