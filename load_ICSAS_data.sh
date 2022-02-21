#!/bin/bash

# abort on error
set -e

# activate venv
source ../stats_racing/venv/bin/activate

# load general data
python3 upsert_championships_leagues.py
python3 upsert_drivers.py
python3 upsert_teams.py

# load data specific to championship and league
python3 upsert_seasons.py -c ICSAS -l A
python3 upsert_seasons.py -c ICSAS -l B
python3 upsert_seasons.py -c ICSAS -l Final

# load data specific to championship, league and season
for season in 1
do
    echo "Events for season $season"
    echo "A"
    python3 upsert_events.py -c ICSAS -l A -s $season
    echo "B"
    python3 upsert_events.py -c ICSAS -l B -s $season
    echo "Final"
    python3 upsert_events.py -c ICSAS -l Final -s $season
done

# now event specific

# races
for season in 1
do
    if [ $season -eq 1 ]
    then
        event_dates_groups="20220109 20220116 20220123"
        event_dates_finals="20220213"
    fi

    for event_date in $event_dates_groups
    do
        echo "Races for season $season and event $event_date"

        echo "A"
        python3 upsert_races.py -c ICSAS -l A -s $season -e $event_date

        echo "B"
        python3 upsert_races.py -c ICSAS -l B -s $season -e $event_date


        echo "Results for season $season and event $event_date"
        echo "A"
        python3 upsert_results.py -c ICSAS -l A -s $season -e $event_date
        
        echo "B"
        python3 upsert_results.py -c ICSAS -l B -s $season -e $event_date
    done

    for event_date in $event_dates_finals
    do
        echo "Final Races"
        python3 upsert_races.py -c ICSAS -l Final -s $season -e $event_date

        echo "Final Results"
        python3 upsert_results.py -c ICSAS -l Final -s $season -e $event_date
    done
done