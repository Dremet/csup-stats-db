drop table if exists base.league;

create table base.league (
    l_id serial primary key,
    c_c_id int not null,
    l_name varchar not null
);