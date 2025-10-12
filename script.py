from sqlmodel import SQLModel, create_engine, Session, select
from models import (
    Venue,
    Pitcher,
    Game,
    GameScore,
    Rating,
)
from datetime import date

engine = create_engine("sqlite:///pitching.db")
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    venue = Venue(id=23, name="Milwaukee County Stadium")
    pitcher = Pitcher(id=124071, name="David Wells")
    game = Game(id=199452, date=date(1990, 6, 10), venue=venue, runs=18)
    game_score = GameScore(game=game, pitcher=pitcher, game_score=39.0)
    rating = Rating(pitcher=pitcher, date=date(1990, 6, 10), rating=500)

    session.add_all([venue, pitcher, game, game_score, rating])
    session.commit()

with Session(engine) as session:
    pitchers = session.exec(select(Pitcher)).all()
    print(pitchers)
