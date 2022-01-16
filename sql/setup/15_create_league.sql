drop table if exists base.leagues;

create table base.leagues (
    l_id serial primary key,
    c_c_id int not null,
    l_name varchar not null,
    UNIQUE (c_c_id, l_name)
);