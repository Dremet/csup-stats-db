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
python3 upsert_seasons.py -c ICSTC -l Superstars
python3 upsert_seasons.py -c ICSTC -l Experts
python3 upsert_seasons.py -c ICSTC -l Pros
python3 upsert_seasons.py -c ICSTC -l "Semi Pros"
python3 upsert_seasons.py -c ICSTC -l Amateur

# load data specific to championship, league and season
for season in 2 3
do
    echo "Teams and Mappings for season $season"

    echo "Superstars"
    python3 upsert_teams_and_mappings.py -c ICSTC -l Superstars -s $season
    echo "Experts"
    python3 upsert_teams_and_mappings.py -c ICSTC -l Experts -s $season
    echo "Pros"
    python3 upsert_teams_and_mappings.py -c ICSTC -l Pros -s $season
    echo "Semi Pros"
    python3 upsert_teams_and_mappings.py -c ICSTC -l "Semi Pros" -s $season
    if [ $season -gt 2 ]
    then
        echo "Amateur"
        python3 upsert_teams_and_mappings.py -c ICSTC -l Amateur -s $season
    fi

    echo "Events for season $season"
    echo "Superstars"
    python3 upsert_events.py -c ICSTC -l Superstars -s $season
    echo "Experts"
    python3 upsert_events.py -c ICSTC -l Experts -s $season
    echo "Pros"
    python3 upsert_events.py -c ICSTC -l Pros -s $season
    echo "Semi Pros"
    python3 upsert_events.py -c ICSTC -l "Semi Pros" -s $season
    if [ $season -gt 2 ]
    then
        echo "Amateur"
        python3 upsert_events.py -c ICSTC -l Amateur -s $season
    fi
done

# now event specific

# races
for season in 2 3
do
    if [ $season -eq 2 ]
    then
        event_dates="20210926 20211003 20211010 20211017 20211024 20211031"
    elif [ $season -eq 3 ]
    then
        event_dates="20220109 20220116 20220123 20220130"
    fi

    for event_date in $event_dates
    do
        echo "Races for season $season and event $event_date"

        echo "Superstars"
        python3 upsert_races.py -c ICSTC -l Superstars -s $season -e $event_date

        if [ $event_date -ne 20220130 ]
        then
            echo "Experts"
            python3 upsert_races.py -c ICSTC -l Experts -s $season -e $event_date
        fi
        
        echo "Pros"
        python3 upsert_races.py -c ICSTC -l Pros -s $season -e $event_date

        if [ $event_date -ne 20210926 ]
        then
            echo "Semi Pros"
            python3 upsert_races.py -c ICSTC -l "Semi Pros" -s $season -e $event_date
        fi

        if [ $season -gt 2 ]
        then
            echo "Amateur"
            python3 upsert_races.py -c ICSTC -l Amateur -s $season -e $event_date
        fi

        echo "Results for season $season and event $event_date"
        echo "Superstars"
        python3 upsert_results.py -c ICSTC -l Superstars -s $season -e $event_date
        
        
        if [ $event_date -ne 20220130 ]
        then
            echo "Experts"
            python3 upsert_results.py -c ICSTC -l Experts -s $season -e $event_date
        fi
        
        echo "Pros"
        python3 upsert_results.py -c ICSTC -l Pros -s $season -e $event_date
        
        if [ $event_date -ne 20210926 ]
        then
            echo "Semi Pros"
            python3 upsert_results.py -c ICSTC -l "Semi Pros" -s $season -e $event_date
        fi

        if [ $season -gt 2 ]
        then
            echo "Amateur"
            python3 upsert_results.py -c ICSTC -l Amateur -s $season -e $event_date
        fi
    done
done