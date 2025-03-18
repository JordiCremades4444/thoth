with calendar_dates as (select
    calendar_date
    from unnest(sequence(date({start_date}),date({end_date}),interval '1' day)) as cte (calendar_date)
    where true
)

select
    p_creation_date,
    order_id,
    order_final_status,
    order_vertical,
    order_total_purchase_eur,
    order_total_purchase_local
from delta.central_order_descriptors_odp.order_descriptors_v2
inner join calendar_dates
    on order_descriptors_v2.p_creation_date = calendar_dates.calendar_date
where true
    and order_city_code in ({cities})
order by 1 asc
