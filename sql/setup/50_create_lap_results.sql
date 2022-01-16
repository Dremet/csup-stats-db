drop table if exists base.lap_results;

create table base.lap_results (
    lr_id serial primary key,
    rr_rr_id int not null,
    lr_lap smallint not null,
    lr_position smallint,
    lr_has_boxed boolean,
    UNIQUE (rr_rr_id, lr_lap)
);