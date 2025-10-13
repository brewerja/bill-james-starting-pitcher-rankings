from datetime import date as date_type
from sqlmodel import SQLModel, Field, Relationship


class Venue(SQLModel, table=True):
    __tablename__ = "venues"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True)

    games: list["Game"] = Relationship(back_populates="venue")
    expected_game_scores: list["ExpectedGameScore"] = Relationship(
        back_populates="venue"
    )


class ExpectedGameScore(SQLModel, table=True):
    __tablename__ = "expected_game_scores"

    venue_id: int | None = Field(
        foreign_key="venues.id", primary_key=True, default=None
    )
    date: date_type = Field(primary_key=True)
    expected_game_score: float

    venue: "Venue" = Relationship(back_populates="expected_game_scores")


class Pitcher(SQLModel, table=True):
    __tablename__ = "pitchers"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True)

    pitcher_outings: list["PitcherOuting"] = Relationship(back_populates="pitcher")
    ratings: list["Rating"] = Relationship(back_populates="pitcher")


class PitcherOuting(SQLModel, table=True):
    __tablename__ = "pitcher_outings"

    game_id: int | None = Field(foreign_key="games.id", primary_key=True, default=None)
    pitcher_id: int | None = Field(
        foreign_key="pitchers.id", primary_key=True, default=None
    )
    outs: int
    ab: int
    batters_faced: int
    hits: int
    runs: int
    earned_runs: int
    home_runs: int
    walks: int
    intentional_walks: int
    strikeouts: int
    wild_pitches: int
    balks: int
    hit_batters: int
    ground_balls: int
    fly_balls: int
    pitches: int
    strikes: int

    game_score: float | None = None

    def __init__(self, **data):
        super().__init__(**data)
        self.game_score = self.calculate_game_score()

    def calculate_game_score(self) -> float:
        return (
            50
            + self.outs
            + max(0, 2 * 12 - self.outs)
            + self.strikeouts
            - 2 * self.hits
            - 4 * self.earned_runs
            - 2 * (self.runs - self.earned_runs)
            - self.walks
        )

    game: "Game" = Relationship(back_populates="pitcher_outings")
    pitcher: "Pitcher" = Relationship(back_populates="pitcher_outings")


class Game(SQLModel, table=True):
    __tablename__ = "games"

    id: int = Field(primary_key=True)
    date: date_type = Field(index=True)
    venue_id: int | None = Field(foreign_key="venues.id", default=None)
    runs: int

    venue: "Venue" = Relationship(back_populates="games")
    pitcher_outings: list["PitcherOuting"] = Relationship(back_populates="game")


class Rating(SQLModel, table=True):
    __tablename__ = "ratings"

    pitcher_id: int = Field(foreign_key="pitchers.id", primary_key=True, default=None)
    date: date_type = Field(primary_key=True)
    rating: float

    pitcher: "Pitcher" = Relationship(back_populates="ratings")
