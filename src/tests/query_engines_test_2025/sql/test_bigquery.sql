with calendar_dates as (select
    calendar_date
    from unnest(generate_date_array(date({start_date}),date({end_date}),interval 1 day)) as calendar_date
    where true
)

select
    *
from `fulfillment-dwh-production.curated_data_shared_experimentation.experiment_assignment_glovo`
where true
    and layersExposureReason in ('EXPERIMENT_ASSIGNMENT')
    and layersIsForcedAssignment = 'false'
    and partition_date in (select calendar_date from calendar_dates)
limit 10
