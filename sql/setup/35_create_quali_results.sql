drop table if exists base.quali_results;

create table base.quali_results (
    q_id serial primary key,
    r_r_id int not null,
    d_d_id int not null,
    q_position smallint,
    q_lap_time_seconds float,
    UNIQUE (r_r_id, d_d_id)
);