insert into base.leagues (
    c_c_id,
    l_name
)
values
(%(c_c_id)s, %(l_name)s)

on conflict (c_c_id, l_name)
do 
update set 
    c_c_id = EXCLUDED.c_c_id
;