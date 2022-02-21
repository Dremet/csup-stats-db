drop table if exists base.elo;

create table base.elo (
    elo_id serial primary key,
    d_d_id int not null,
    elo_ranking float not null,
    elo_date date not null,
    UNIQUE (d_d_id, elo_date)
);