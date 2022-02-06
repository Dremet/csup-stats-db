insert into base.race_results (
    r_r_id,
    d_d_id,
    rr_position,
    rr_race_time_seconds,
    rr_lappings,
    rr_fastest_lap_seconds,
    rr_got_penalty,
    rr_penalty_description
)
values
(%(r_r_id)s, %(d_d_id)s, %(position)s, %(race_time_seconds)s, %(lappings)s, %(fastest_lap_seconds)s, %(penalty)s, %(penalty_description)s)
on conflict (r_r_id, d_d_id)
do
update set
    r_r_id = EXCLUDED.r_r_id,
    d_d_id = EXCLUDED.d_d_id,
    rr_position = EXCLUDED.rr_position,
    rr_race_time_seconds = EXCLUDED.rr_race_time_seconds,
    rr_lappings = EXCLUDED.rr_lappings,
    rr_fastest_lap_seconds = EXCLUDED.rr_fastest_lap_seconds,
    rr_got_penalty = EXCLUDED.rr_got_penalty,
    rr_penalty_description = EXCLUDED.rr_penalty_description
;
