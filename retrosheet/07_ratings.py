from sqlmodel import (
    Session,
    SQLModel,
    create_engine,
    select,
)

from models import Pitcher

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/mydb")
SQLModel.metadata.create_all(engine)


def process_pitcher_ratings(session: Session, pitcher: Pitcher) -> None:
    prev_outing = None
    for i, outing in enumerate(sorted(pitcher.outings, key=lambda o: o.game.date)):
        if prev_outing:
            days_inactive = (outing.game.date - prev_outing.game.date).days
            if days_inactive < 7:
                current_rating = prev_outing.rating
            elif days_inactive <= 200:
                current_rating = prev_outing.rating - 0.25 * (days_inactive - 6)
            else:
                current_rating = prev_outing.rating - 0.25 * 194 - (days_inactive - 200)
        else:  # Everyone starts at 300
            current_rating = 300

        runs_at_venue_last_100_days = outing.game.runs_at_venue_last_100_days
        if runs_at_venue_last_100_days:
            r = outing.game.runs_at_venue_last_100_days / 100
            e = 68 - 2 * r
            adjusted_game_score = 50 + outing.game_score - e
        else:
            adjusted_game_score = outing.game_score
        new_rating = current_rating * 0.97 + 0.30 * adjusted_game_score
        outing.rating = new_rating
        session.add(outing)

        prev_outing = outing


if __name__ == "__main__":
    with Session(engine) as session:
        for pitcher in session.exec(select(Pitcher)).all():
            process_pitcher_ratings(session, pitcher)
            session.commit()
