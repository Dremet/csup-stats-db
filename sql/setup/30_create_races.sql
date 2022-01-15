drop table if exists base.races;

create table base.races (
    r_id serial primary key,
    e_e_id int,
    r_track varchar not null,
    r_version varchar not null,
    r_reversed boolean default FALSE,
    r_laps smallint not null,
    r_car varchar not null,
    r_class varchar not null,
    r_tire_wear smallint,
    r_fuel_consumption smallint,
    r_damage_cars smallint,
    r_damage_environment smallint,
    r_drafting smallint,
    r_is_ghost_race boolean default FALSE,
    r_has_reversed_grid boolean default FALSE,
    r_details_were_announced boolean default FALSE
);