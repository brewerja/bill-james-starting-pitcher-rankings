from sqlmodel import Session, SQLModel, create_engine, select, func, cast, Integer

from models import Game

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/mydb")
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    for game in session.exec(select(Game).order_by(Game.date)):
        print(game.date, game.id)
        subquery = (
            select(Game.visitor_runs, Game.home_runs)
            .where(
                Game.venue_id == game.venue_id,
                cast(func.substr(Game.id, 4), Integer)
                < cast(func.substr(game.id, 4), Integer),
            )
            .order_by(Game.id.desc())
            .limit(100)
            .subquery()
        )

        # Count the number of rows in the subquery
        count_query = select(func.count()).select_from(subquery)
        num_games = session.exec(count_query).one()

        # If fewer than 100 prior games, return None
        if num_games < 100:
            grand_total = None
        else:
            statement = select(func.sum(subquery.c.visitor_runs + subquery.c.home_runs))
            grand_total = session.exec(statement).one()

        game.runs_at_venue_last_100_days = grand_total
        session.add(game)
    session.commit()
