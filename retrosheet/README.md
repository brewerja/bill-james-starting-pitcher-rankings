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
