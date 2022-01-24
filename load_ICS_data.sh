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
python3 upsert_teams_and_mappings.py -c ICSTC -l Superstars -s 2
python3 upsert_teams_and_mappings.py -c ICSTC -l Experts -s 2
python3 upsert_teams_and_mappings.py -c ICSTC -l Pros -s 2
python3 upsert_teams_and_mappings.py -c ICSTC -l "Semi Pros" -s 2
python3 upsert_teams_and_mappings.py -c ICSTC -l Amateur -s 2

python3 upsert_events.py -c ICSTC -l Superstars -s 2
python3 upsert_events.py -c ICSTC -l Experts -s 2
python3 upsert_events.py -c ICSTC -l Pros -s 2
python3 upsert_events.py -c ICSTC -l "Semi Pros" -s 2
python3 upsert_events.py -c ICSTC -l Amateur -s 2

# now event specific

# races
python3 upsert_races.py -c ICSTC -l Superstars -s 2 -e 20220109
python3 upsert_races.py -c ICSTC -l Experts -s 2 -e 20220109
python3 upsert_races.py -c ICSTC -l Pros -s 2 -e 20220109
python3 upsert_races.py -c ICSTC -l "Semi Pros" -s 2 -e 20220109
python3 upsert_races.py -c ICSTC -l Amateur -s 2 -e 20220109

python3 upsert_races.py -c ICSTC -l Superstars -s 2 -e 20220116
python3 upsert_races.py -c ICSTC -l Experts -s 2 -e 20220116
python3 upsert_races.py -c ICSTC -l Pros -s 2 -e 20220116
python3 upsert_races.py -c ICSTC -l "Semi Pros" -s 2 -e 20220116
python3 upsert_races.py -c ICSTC -l Amateur -s 2 -e 20220116

# results
python3 upsert_results.py -c ICSTC -l Superstars -s 2 -e 20220109
python3 upsert_results.py -c ICSTC -l Experts -s 2 -e 20220109
python3 upsert_results.py -c ICSTC -l Pros -s 2 -e 20220109
python3 upsert_results.py -c ICSTC -l "Semi Pros" -s 2 -e 20220109
python3 upsert_results.py -c ICSTC -l Amateur -s 2 -e 20220109

python3 upsert_results.py -c ICSTC -l Superstars -s 2 -e 20220116
python3 upsert_results.py -c ICSTC -l Experts -s 2 -e 20220116
python3 upsert_results.py -c ICSTC -l Pros -s 2 -e 20220116
python3 upsert_results.py -c ICSTC -l "Semi Pros" -s 2 -e 20220116
python3 upsert_results.py -c ICSTC -l Amateur -s 2 -e 20220116
