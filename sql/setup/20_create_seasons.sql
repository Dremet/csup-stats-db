drop table if exists base.seasons;

create table base.seasons (
    s_id serial primary key,
    l_l_id int not null,
    s_desc varchar not null
);