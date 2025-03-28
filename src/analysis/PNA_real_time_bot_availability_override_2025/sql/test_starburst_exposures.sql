with calendar_dates as (select
    calendar_date
    from unnest(sequence(date({start_date}),date({end_date}),interval '1' day)) as cte (calendar_date)
    where true
)

select
    p_partition_date,
    experiment_variation,
    count(distinct randomization_unit_id) as n_customer_id
from delta.customer__funwithflags_experiment_assignments_daily__odp.funwithflags_experiment_assignments_daily
where true
    and p_partition_date in (select calendar_date from calendar_dates)
    and experiment_id = 'PNA_real_time_bot_availability_override'
group by 1,2
order by 1,2
