with calendar_dates as (select
    calendar_date
    from unnest(generate_date_array(date({start_date}),date({end_date}),interval '1' day)) as calendar_date
    where true
)

select
    partition_date,
    experimentVariation,
    count(distinct randomizationUnitId) as n_customer_id
from `fulfillment-dwh-production.curated_data_shared_experimentation.experiment_assignment_glovo`
where true
    and partition_date in (select calendar_date from calendar_dates)
    and experimentID = 'PNA_real_time_bot_availability_override'
group by 1,2
order by 1,2
