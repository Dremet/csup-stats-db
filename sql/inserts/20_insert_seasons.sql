insert into base.seasons (
    l_l_id,
    s_desc
)
values
(%(l_l_id)s, %(s_desc)s)

on conflict (l_l_id, s_desc)
do nothing
;