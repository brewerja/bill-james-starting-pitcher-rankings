from sqlmodel import (
    Session,
    SQLModel,
    create_engine,
    select,
    func,
    cast,
    Integer,
    update,
    case,
)

from models import Game

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/mydb")
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    numeric_id = cast(func.substr(Game.id, 4), Integer)

    # Use window functions to get both row number and sum over the window
    row_number = func.row_number().over(partition_by=Game.venue_id, order_by=numeric_id)

    sum_last_100 = func.sum(Game.visitor_runs + Game.home_runs).over(
        partition_by=Game.venue_id, order_by=numeric_id, rows=(-100, -1)
    )

    # Only keep the sum if there are at least 100 prior rows
    conditional_sum = case((row_number >= 100, sum_last_100), else_=None).label(
        "runs_at_venue_last_100_games"
    )

    subquery = select(Game.id.label("game_id"), conditional_sum).subquery()

    session.exec(
        update(Game)
        .values(runs_at_venue_last_100_games=subquery.c.runs_at_venue_last_100_games)
        .where(Game.id == subquery.c.game_id)
    )
    session.commit()
