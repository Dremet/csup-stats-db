drop table if exists base.championships;

create table base.championships (
    c_id serial primary key,
    c_name varchar unique not null,
    c_has_teams boolean not null,
    c_region varchar default 'World'
);

alter table base.championships
add column c_description text;