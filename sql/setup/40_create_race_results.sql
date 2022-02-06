drop table if exists base.race_results;

create table base.race_results (
    rr_id serial primary key,
    r_r_id int not null,
    d_d_id int not null,
    rr_position smallint,
    rr_race_time_seconds float,
    rr_lappings int default 0,
    rr_fastest_lap_seconds float,
    UNIQUE (r_r_id, d_d_id)
);

alter table base.race_results
add column rr_got_penalty boolean,
add column rr_penalty_description text;