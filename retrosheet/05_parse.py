#!/usr/bin/env python

import csv
import itertools
import os
import re
from datetime import date

import lxml.etree
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, SQLModel, create_engine

from models import Game, Pitcher, PitcherOuting, Venue

PEOPLE_CSV_FILE = "people.csv"
VENUE_CSV_FILE = "venues.csv"

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/mydb")
SQLModel.metadata.create_all(engine)


def build_people_lookup():
    with open(PEOPLE_CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {
            row["key_retro"]: {
                "key_mlbam": int(row["key_mlbam"]),
                "name_last": row["name_last"],
                "name_first": row["name_first"],
            }
            for row in reader
        }


people_lookup = build_people_lookup()


def persist_venues() -> None:
    with open(VENUE_CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        with Session(engine) as session:
            for row in reader:
                session.add(
                    Venue(
                        id=row["key_retro"],
                        mlbam_id=int(row["key_mlbam"]),
                        name=row["venue_name"],
                    )
                )
            session.commit()


def persist_pitchers_games_outings(xml_file: str) -> None:
    with open(xml_file) as f:
        doc = lxml.etree.fromstringlist(itertools.chain("<games>", f, "</games>"))
        pitchers, games, outings = {}, [], []

        for boxscore in doc.findall("boxscore"):
            # Skip an all star game that's mixed in
            if boxscore.get("game_id") == "ASE196108200":
                continue
            date_str = boxscore.get("date").replace("/", "-")
            linescore = boxscore.find("linescore")
            games.append(
                Game(
                    id=boxscore.get("game_id"),
                    date=date.fromisoformat(date_str),
                    venue_id=boxscore.get("site"),
                    visitor=boxscore.get("visitor"),
                    visitor_city=boxscore.get("visitor_city"),
                    visitor_name=boxscore.get("visitor_name"),
                    visitor_runs=int(linescore.get("away_runs")),
                    home=boxscore.get("home"),
                    home_city=boxscore.get("home_city"),
                    home_name=boxscore.get("home_name"),
                    home_runs=int(linescore.get("home_runs")),
                )
            )

            for pitcher in boxscore.xpath(".//pitching/pitcher[@gs='1']"):
                p = pitcher.attrib
                pitcher_id = p["id"]
                if pitcher_id not in pitchers:
                    pitchers[pitcher_id] = Pitcher(
                        id=pitcher_id,
                        mlbam_id=people_lookup[pitcher_id]["key_mlbam"],
                        name=f"{p['fname']} {p['lname']}",
                    )
                outings.append(
                    PitcherOuting(
                        game_id=boxscore.get("game_id"),
                        pitcher_id=pitcher_id,
                        outs=int(p["outs"]),
                        ab=int(p["ab"]),
                        batters_faced=int(p["bf"]),
                        hits=int(p["h"]),
                        runs=int(p["r"]),
                        earned_runs=int(p["er"]),
                        home_runs=int(p["hr"]),
                        walks=int(p["bb"]),
                        intentional_walks=int(p["ibb"]),
                        strikeouts=int(p["so"]),
                        wild_pitches=int(p["wp"]),
                        balks=int(p["bk"]),
                        hit_batters=int(p["hb"]),
                        ground_balls=int(p["gb"]),
                        fly_balls=int(p["fb"]),
                        pitches=None if not p.get("pitch") else int(p["pitch"]),
                        strikes=None if not p.get("strike") else int(p["strike"]),
                    )
                )

    with Session(engine) as session:
        session.exec(
            insert(Pitcher)
            .values([p.model_dump() for p in pitchers.values()])
            .on_conflict_do_nothing(index_elements=["id"])
        )
        session.add_all(games + outings)
        session.commit()


def get_boxscore_xml_files(base_dirs: list[str]) -> list[str]:
    pattern = re.compile(r"(\d{4})\.xml$")
    xml_files: list[str] = []
    for base_dir in base_dirs:
        for root, _, files in os.walk(base_dir):
            for file in files:
                match = pattern.search(file)
                if match:
                    year = int(match.group(1))
                    if year >= 1960:
                        xml_files.append(os.path.join(root, file))
    return xml_files


if __name__ == "__main__":
    persist_venues()
    base_dirs = ["regular_season/box_scores", "postseason/box_scores"]
    for boxscore_xml_file in sorted(get_boxscore_xml_files(base_dirs)):
        print(boxscore_xml_file)
        persist_pitchers_games_outings(boxscore_xml_file)
