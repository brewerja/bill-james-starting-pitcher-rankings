from typing import cast
from datetime import datetime, date
from typing import TypedDict

import statsapi


class Game(TypedDict):
    id: int
    date: date
    datetime: datetime
    game_type: str
    venue_id: int
    venue_name: str
    away_name: str
    away_score: int
    home_name: str
    home_score: int
    status: str


# Needs:
# Going back 100 games, store the number of runs scored in the venue each game
# Each day, calculcate game scores for all starting pitchers


def main(date_str: str) -> None:
    response = statsapi.schedule(start_date=date_str, end_date=date_str)
    for game in response:
        g = build_game(game)
        print(g)

        response = statsapi.boxscore_data(gamePk=g["id"])
        away_starter_id = response["away"]["pitchers"][0]
        away_starter_stats = response["away"]["players"][f"ID{away_starter_id}"][
            "stats"
        ]["pitching"]
        away_starter = response["away"]["players"][f"ID{away_starter_id}"]
        print(away_starter["person"]["fullName"])
        print(away_starter_stats)
        print(away_starter_id, calculate_game_score(away_starter_stats))
        home_starter_id = response["home"]["pitchers"][0]
        home_starter_stats = response["home"]["players"][f"ID{home_starter_id}"][
            "stats"
        ]["pitching"]
        home_starter = response["home"]["players"][f"ID{home_starter_id}"]
        print(home_starter["person"]["fullName"])
        print(home_starter_stats)
        print(home_starter_id, calculate_game_score(home_starter_stats))
        break


def calculate_game_score(stats: dict[str, int]) -> int:
    # GSc = 50 + outs + 2*IP>4 + K - 2H - 4ER - 2UER - W
    innings_str, extra_outs_str = cast(str, stats["inningsPitched"]).split(".")
    return (
        50
        + int(innings_str) * 3
        + int(extra_outs_str)
        + 2 * (int(innings_str) - 4)
        + stats["strikeOuts"]
        - 2 * stats["hits"]
        - 4 * stats["earnedRuns"]
        - 2 * (stats["runs"] - stats["earnedRuns"])
        - stats["baseOnBalls"]
    )


def build_game(game) -> Game:
    return Game(
        id=game["game_id"],
        date=date.fromisoformat(game["game_date"]),
        datetime=datetime.fromisoformat(game["game_datetime"].replace("Z", "+00:00")),
        game_type=game["game_type"],
        venue_id=game["venue_id"],
        venue_name=game["venue_name"],
        away_name=game["away_name"],
        away_score=game["away_score"],
        home_name=game["home_name"],
        home_score=game["home_score"],
        status=game["status"],
    )


if __name__ == "__main__":
    month = 6
    day = 10
    year = 1990
    main(f"{month}/{day}/{year}")
