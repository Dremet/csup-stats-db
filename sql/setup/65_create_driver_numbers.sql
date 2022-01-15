drop table if exists base.driver_numbers;

create table base.driver_numbers (
    dn_id serial primary key,
    d_d_id int not null,
    s_s_id int not null
);