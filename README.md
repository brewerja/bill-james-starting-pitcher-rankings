# Bill James Pitcher Rankings System

[Original Article](http://www.billjamesonline.com/the_worlds_1_starting_pitcher/)

Everybody starts with a ranking of 300.000, and you can't go lower than 300, even if you pitch badly.

When a pitcher makes a start, we:

1. Mark down his previous ranking by 3%
2. Add 30% of his Game Score for the start

## Game Score

Start with 50 points. Add 1 point for each out recorded, (or 3 points per inning). Add 2 points for each inning completed after the 4th. Add 1 point for each strikeout. Subtract 2 points for each hit allowed. Subtract 4 points for each earned run allowed. Subtract 2 points for each unearned run allowed. Subtract 1 point for each walk.

## Inactivity

1. If a pitcher does not make a start for 1 to 6 days, his score does not change. It remains whatever it was after his last start.

2. On days 7 to 200, if a pitcher does not make a start (for seven days or more), we reduce his ranking by one-quarter of a point for each day that he is inactive—in season or off season. During the off-season everybody moves down, but everybody moves down in lock-step, so the rankings don’t change once you get 7 days from the end of the season.

3. If the pitcher remains inactive for more than 200 days, we reduce his score by one point per day beginning with the 201st day.

## Park Effects

For park effects, we park-adjust Game Scores. Take the average number of runs per game scored in the last 100 games played in the park; call that number R. The expected Game Score in a game is:

68 minus two times R

which we will call "E" for "expected Game Score".

E = 68 – 2R

Then you adjust the Game Score by adding 50, and subtracting E. GS is "Game Score" and AGS is "Adjusted Game Score":

AGS = 50 + GS – E

## Starting Point

OK, the problem is where to start. The only really accurate place to start the rankings is would be in 1876, but of course we don’t have organized data for every start prior to 1960. Bill James started his rankings with the 1990 season.
