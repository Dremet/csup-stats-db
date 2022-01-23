insert into base.quali_results (
    r_r_id,
    d_d_id,
    q_position,
    q_lap_time_seconds
)
values
(%(r_r_id)s, %(d_d_id)s, %(position)s, %(quali_lap_time_seconds)s)
on conflict (r_r_id, d_d_id)
do
update set
    r_r_id = EXCLUDED.r_r_id,
    d_d_id = EXCLUDED.d_d_id,
    q_position = EXCLUDED.q_position,
    q_lap_time_seconds = EXCLUDED.q_lap_time_seconds
;