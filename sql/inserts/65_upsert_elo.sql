insert into base.elo (
    d_d_id,
    elo_ranking,
    elo_date
)
values
(%(d_d_id)s, %(elo_ranking)s, %(elo_date)s)

on conflict (d_d_id, elo_date)
do 
update set 
    elo_ranking = EXCLUDED.elo_ranking
;