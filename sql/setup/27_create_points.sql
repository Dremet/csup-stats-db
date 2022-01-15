drop table if exists base.event_points;

create table base.event_points (
    p_id serial primary key,
    e_e_id int,
    d_d_id int,
    p_amount int default 0
);