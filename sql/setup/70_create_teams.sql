drop table if exists base.teams;

create table base.teams (
    t_id int unique not null,
    t_name varchar not null,
    t_tag varchar,
    t_primary_color varchar,
    t_secondary_color varchar,
    t_tertiary_color varchar
);