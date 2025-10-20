# Instructions to Process Historical Data

Procedure:
 - Download the events (regular and post season) and ballparks from Retrosheet.
 - Install chadwick: `brew install chadwick`
 - Build the boxscores using chadwick
 - Build conversion tables for Retrosheet to MLBAM ids for people and ballparks.
 - Parse the boxscores to create games and pitcher outings.

Pitcher and ballpark ids are able to be converted to MLBAM ids.
Main reason to prefer MLBAM ids is that's what will be used during the season from MLB's API.

Need to use Retrosheet game ids for historical games, new games could use MLBAM ids as it's live populating.
It might make sense to convert the MLBAM ids to Retrosheet ids in the offseason once Retrosheet releases a season.

For some reason the ballparks endpoint on MLBAM doesn't include the retrosheet ids for a few ballparks.

```
```
```
```
SELECT
  po.game_id,
  g.date,
  p.name,
  po.game_score
FROM pitcher_outings AS po
INNER JOIN games AS g
  ON po.game_id = g.id
INNER JOIN pitchers AS p
  ON po.pitcher_id = p.id
ORDER BY po.game_score DESC
LIMIT 100;


Ballparks endpoint from MLBAM has some retrosheet IDs, but not all.
Need to look for a match.

```
COPY (
SELECT
  po.game_id,
  g.date,
  g.venue_id,
  g.runs_at_venue_last_100_games as rlast100,
  po.pitcher_id,
  po.game_score,
  round(po.rating, 2) as rating,
  g.date - LAG(g.date) OVER (
    PARTITION BY po.pitcher_id
    ORDER BY g.date
  ) -1 AS days_inactive,
  50 + po.game_score - (68 - 2 * g.runs_at_venue_last_100_games::numeric / 100) as ags
FROM pitcher_outings AS po
JOIN games AS g
  ON po.game_id = g.id
WHERE po.pitcher_id = 'glast001'
ORDER BY g.date
) TO '/exports/glast001.csv' WITH CSV HEADER;
```
