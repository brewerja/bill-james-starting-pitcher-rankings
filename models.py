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

    game_scores: list["GameScore"] = Relationship(back_populates="pitcher")
    ratings: list["Rating"] = Relationship(back_populates="pitcher")


class GameScore(SQLModel, table=True):
    __tablename__ = "game_scores"

    game_id: int | None = Field(foreign_key="games.id", primary_key=True, default=None)
    pitcher_id: int | None = Field(
        foreign_key="pitchers.id", primary_key=True, default=None
    )
    game_score: float

    game: "Game" = Relationship(back_populates="game_scores")
    pitcher: "Pitcher" = Relationship(back_populates="game_scores")


class Game(SQLModel, table=True):
    __tablename__ = "games"

    id: int = Field(primary_key=True)
    date: date_type = Field(index=True)
    venue_id: int | None = Field(foreign_key="venues.id", default=None)
    runs: int

    venue: "Venue" = Relationship(back_populates="games")
    game_scores: list["GameScore"] = Relationship(back_populates="game")


class Rating(SQLModel, table=True):
    __tablename__ = "ratings"

    pitcher_id: int = Field(foreign_key="pitchers.id", primary_key=True, default=None)
    date: date_type = Field(primary_key=True)
    rating: float

    pitcher: "Pitcher" = Relationship(back_populates="ratings")
