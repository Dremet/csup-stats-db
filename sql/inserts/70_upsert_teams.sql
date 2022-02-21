insert into base.teams (
    t_id,
    t_name,
    t_tag,
    t_primary_color,
    t_secondary_color,
    t_tertiary_color
)
values
(%(id)s, %(name)s, %(tag)s, %(primary_color)s, %(secondary_color)s, %(tertiary_color)s)

on conflict (t_id)
do 
update set
    t_name = EXCLUDED.t_name,
    t_tag = EXCLUDED.t_tag,
    t_primary_color = EXCLUDED.t_primary_color,
    t_secondary_color = EXCLUDED.t_secondary_color,
    t_tertiary_color = EXCLUDED.t_tertiary_color
;