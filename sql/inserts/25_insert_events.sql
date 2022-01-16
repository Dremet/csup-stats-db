insert into base.events(
    s_s_id,
    e_date,
    e_uses_event_points,
    e_points_pos_1,
    e_points_pos_2,
    e_points_pos_3,
    e_points_pos_4,
    e_points_pos_5,
    e_points_pos_6,
    e_points_pos_7,
    e_points_pos_8,
    e_points_pos_9,
    e_points_pos_10,
    e_points_pos_11,
    e_points_pos_12,
    e_points_for_pole,
    e_points_for_fastest_lap
)
values
(
    %(s_s_id)s,
    %(e_date)s,
    %(e_uses_event_points)s,
    %(e_points_pos_1)s,
    %(e_points_pos_2)s,
    %(e_points_pos_3)s,
    %(e_points_pos_4)s,
    %(e_points_pos_5)s,
    %(e_points_pos_6)s,
    %(e_points_pos_7)s,
    %(e_points_pos_8)s,
    %(e_points_pos_9)s,
    %(e_points_pos_10)s,
    %(e_points_pos_11)s,
    %(e_points_pos_12)s,
    %(e_points_for_pole)s,
    %(e_points_for_fastest_lap)s
)
on conflict (s_s_id, e_date)
do 
update set 
    e_uses_event_points = EXCLUDED.e_uses_event_points,
    e_points_pos_1 = EXCLUDED.e_points_pos_1,
    e_points_pos_2 = EXCLUDED.e_points_pos_2,
    e_points_pos_3 = EXCLUDED.e_points_pos_3,
    e_points_pos_4 = EXCLUDED.e_points_pos_4,
    e_points_pos_5 = EXCLUDED.e_points_pos_5,
    e_points_pos_6 = EXCLUDED.e_points_pos_6,
    e_points_pos_7 = EXCLUDED.e_points_pos_7,
    e_points_pos_8 = EXCLUDED.e_points_pos_8,
    e_points_pos_9 = EXCLUDED.e_points_pos_9,
    e_points_pos_10 = EXCLUDED.e_points_pos_10,
    e_points_pos_11 = EXCLUDED.e_points_pos_11,
    e_points_pos_12 = EXCLUDED.e_points_pos_12,
    e_points_for_pole = EXCLUDED.e_points_for_pole,
    e_points_for_fastest_lap = EXCLUDED.e_points_for_fastest_lap
;