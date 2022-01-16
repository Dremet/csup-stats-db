insert into base.championships (
    c_name,
    c_has_teams,
    c_region
)
values
(%(c_name)s, %(c_has_teams)s, %(c_region)s)
on conflict (c_name)
do 
update set 
    c_has_teams = EXCLUDED.c_has_teams,
    c_region = EXCLUDED.c_region
RETURNING c_id,c_name
;