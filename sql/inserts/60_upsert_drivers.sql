insert into base.drivers (
    d_id,
    d_name,
    d_two_letter_country_code,
    d_two_letter_continent_code,
    d_steering_device
)
values
(%(d_id)s, %(d_name)s, %(d_two_letter_country_code)s, %(d_two_letter_continent_code)s, %(d_steering_device)s)

on conflict (d_id)
do 
update set 
    d_name = EXCLUDED.d_name,
    d_two_letter_country_code = EXCLUDED.d_two_letter_country_code,
    d_two_letter_continent_code = EXCLUDED.d_two_letter_continent_code,
    d_steering_device = EXCLUDED.d_steering_device
;