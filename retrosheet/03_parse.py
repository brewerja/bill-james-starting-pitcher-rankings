#!/usr/bin/env python

import csv
import itertools
from lxml import etree
from datetime import date
from pprint import pprint

from typing import TypedDict


class Outing(TypedDict):
    date: date
    pitcher: dict[str, str]
    site: str
    pitcher_id: str


class RetrosheetGame(TypedDict):
    id: str
    date: date
    site: str
    visitor: str
    visitor_city: str
    visitor_name: str
    visitor_runs: int
    home: str
    home_name: str
    home_city: str
    home_runs: int


INPUT_FILE = "people.csv"


def build_lookup():
    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {
            row["key_retro"]: {
                "key_mlbam": row["key_mlbam"],
                "name_last": row["name_last"],
                "name_first": row["name_first"],
            }
            for row in reader
        }


def parse_for_starting_pitcher_outings(xml_file):
    retro_to_mlbam_lookup = build_lookup()
    with open(xml_file) as f:
        it = itertools.chain("<games>", f, "</games>")
        doc = etree.fromstringlist(it)
        pitcher_outings = []
        games = []
        for boxscore in doc.findall("boxscore"):
            date_str = boxscore.get("date").replace("/", "-")
            linescore = boxscore.find("linescore")
            g = RetrosheetGame(
                id=boxscore.get("game_id"),
                date=date.fromisoformat(date_str),
                site=boxscore.get("site"),
                visitor=boxscore.get("visitor"),
                visitor_city=boxscore.get("visitor_city"),
                visitor_name=boxscore.get("visitor_name"),
                visitor_runs=int(linescore.get("away_runs")),
                home=boxscore.get("home"),
                home_city=boxscore.get("home_city"),
                home_name=boxscore.get("home_name"),
                home_runs=int(linescore.get("home_runs")),
            )
            games.append(g)

            # <boxscore game_id="ANA202404050" date="2024/04/05" site="ANA01"
            # visitor="BOS" visitor_city="Boston" visitor_name="Red Sox"
            # home="ANA" home_city="Anaheim" home_name="Angels"
            # start_time="6:38PM" day_night="night" temperature="54" wind_direction="ltor"
            for pitching in boxscore.findall("pitching"):
                for pitcher in pitching.findall("pitcher"):
                    # {'': 'crawk001', 'lname': 'Crawford', 'fname': 'Kutter',
                    #'gs': '1', 'cg': '0', 'sho': '0', 'gf': '0', 'outs': '14',
                    # 'ab': '17', 'bf': '20', 'h': '2', 'r': '1', 'er': '1', 'hr': '0',
                    # 'bb': '3', 'ibb': '0', 'so': '5', 'wp': '0', 'bk': '0', 'hb': '0',
                    # 'gb': '3', 'fb': '6', 'pitch': '90', 'strike': '56'}
                    if pitcher.attrib["gs"] == "1":
                        pitcher_outings.append(
                            Outing(
                                date=date.fromisoformat(date_str),
                                pitcher=pitcher.attrib,
                                site=boxscore.get("site"),
                                pitcher_id=retro_to_mlbam_lookup[pitcher.attrib["id"]][
                                    "key_mlbam"
                                ],
                            )
                        )
                        break  # only need the starter

    return pitcher_outings, games


if __name__ == "__main__":
    outings, games = parse_for_starting_pitcher_outings(
        "regular_season/box_scores/2024.xml"
    )
    for outing in outings:
        pprint(outing)
    for game in games:
        pprint(game)
