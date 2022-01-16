drop table if exists base.drivers;

create table base.drivers (
    d_id int unique not null,
    d_name varchar unique not null,
    d_two_letter_country_code varchar(2),
    d_two_letter_continent_code varchar(2),
    d_steering_device varchar,
    d_elo float default 1000.0
);