with calendar_dates as (select
    calendar_date
    from unnest(sequence(date({start_date}),date({end_date}),interval '1' day)) as cte (calendar_date)
    where true
)

select
    p_creation_date,
    order_country_code,
    order_final_status,
    count(distinct order_id) as n_orders
from delta.central_order_descriptors_odp.order_descriptors_v2
where true
    and p_creation_date in (select calendar_date from calendar_dates)
    and order_country_code in ('ES','PT')
group by 1,2,3
order by 1,2,3,4
