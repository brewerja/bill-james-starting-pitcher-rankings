#!/bin/bash

# Download ballparks
mkdir -p ballparks/archives
cd ballparks
wget https://www.retrosheet.org/ballparks.zip
unzip ballparks.zip
mv *.zip archives
cd ..

# Download all years from 1960-2024 by decades
mkdir -p regular_season/archives
cd regular_season
wget https://www.retrosheet.org/events/1960seve.zip
wget https://www.retrosheet.org/events/1970seve.zip
wget https://www.retrosheet.org/events/1980seve.zip
wget https://www.retrosheet.org/events/1990seve.zip
wget https://www.retrosheet.org/events/2000seve.zip
wget https://www.retrosheet.org/events/2010seve.zip
wget https://www.retrosheet.org/events/2020seve.zip
mkdir events
mkdir box_scores
unzip \*.zip -d events
mv *.zip archives
cd ..

# Download all postseason data
mkdir -p postseason/archives
cd postseason
wget https://www.retrosheet.org/events/allpost.zip
mkdir events
mkdir box_scores
unzip allpost.zip -d events
mv *.zip archives
cd ..
