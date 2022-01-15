drop table if exists base.race_results;

create table base.race_results (
    rr_id serial primary key,
    r_r_id int not null,
    d_d_id int not null,
    rr_position smallint not null,
    rr_race_time_seconds float not null,
    rr_lappings int default 0,
    rr_fastest_lap_seconds float not null
);