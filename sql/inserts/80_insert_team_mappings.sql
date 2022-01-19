insert into base.team_mappings (
    d_d_id,
    t_t_id,
    s_s_id
)
values
(%(d_d_id)s, %(t_t_id)s, %(s_s_id)s)

on conflict (d_d_id, t_t_id, s_s_id)
do nothing
;