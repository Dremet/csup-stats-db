drop table if exists base.events;

create table base.events (
    e_id serial primary key,
    s_s_id int not null,
    e_date date not null,
    e_uses_event_points boolean not null,
    e_points_pos_1 smallint not null,
    e_points_pos_2 smallint not null,
    e_points_pos_3 smallint not null,
    e_points_pos_4 smallint not null,
    e_points_pos_5 smallint not null,
    e_points_pos_6 smallint not null,
    e_points_pos_7 smallint not null,
    e_points_pos_8 smallint not null,
    e_points_pos_9 smallint not null,
    e_points_pos_10 smallint not null,
    e_points_pos_11 smallint not null,
    e_points_pos_12 smallint not null,
    e_points_for_pole smallint not null,
    e_points_for_fastest_lap smallint not null,
    UNIQUE (s_s_id, e_date)
);