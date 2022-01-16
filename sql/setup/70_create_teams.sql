drop table if exists base.teams;

create table base.teams (
    t_id int unique not null,
    t_name varchar unique not null,
    t_tag varchar unique not null,
    t_primary_color varchar,
    t_secondary_color varchar,
    t_tertiary_color varchar
);