insert into base.races (
    e_e_id,
    r_order,
    r_track,
    r_version,
    r_reversed ,
    r_laps,
    r_car,
    r_class,
    r_tire_wear,
    r_fuel_consumption,
    r_damage_cars,
    r_damage_environment,
    r_drafting,
    r_is_ghost_race,
    r_has_reversed_grid,
    r_details_were_announced 
)
values
(%(e_e_id)s, %(order)s, %(track)s, %(version)s, %(reversed)s, %(laps)s, %(car)s
, %(class)s, %(tire_wear)s, %(fuel_consumption)s, %(damage_cars)s, %(damage_environment)s
, %(drafting)s, %(is_ghost_race)s, %(has_reversed_grid)s, %(details_were_announced)s)
on conflict (e_e_id, r_order)
do 
update set
    r_track = EXCLUDED.r_track,
    r_version = EXCLUDED.r_version,
    r_reversed = EXCLUDED.r_reversed,
    r_laps = EXCLUDED.r_laps,
    r_car = EXCLUDED.r_car,
    r_class = EXCLUDED.r_class,
    r_tire_wear = EXCLUDED.r_tire_wear,
    r_fuel_consumption = EXCLUDED.r_fuel_consumption,
    r_damage_cars = EXCLUDED.r_damage_cars,
    r_damage_environment = EXCLUDED.r_damage_environment,
    r_drafting = EXCLUDED.r_drafting,
    r_is_ghost_race = EXCLUDED.r_is_ghost_race,
    r_has_reversed_grid = EXCLUDED.r_has_reversed_grid,
    r_details_were_announced = EXCLUDED.r_details_were_announced
;