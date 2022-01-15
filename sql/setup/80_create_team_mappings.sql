drop table if exists base.team_mappings;

create table base.team_mappings (
    tm_id serial primary key,
    d_d_id int not null,
    t_t_id int not null,
    s_s_id int not null
);