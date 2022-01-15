drop table if exists base.championship;

create table base.championship (
    c_id serial primary key,
    c_name varchar not null,
    c_has_teams boolean not null,
    c_region varchar default 'World'
);