insert into base.championships (
    c_name,
    c_has_teams,
    c_region,
    c_description
)
values
(%(c_name)s, %(c_has_teams)s, %(c_region)s, %(c_description)s)
on conflict (c_name)
do 
update set 
    c_has_teams = EXCLUDED.c_has_teams,
    c_region = EXCLUDED.c_region,
    c_description = EXCLUDED.c_description
RETURNING c_id,c_name
;