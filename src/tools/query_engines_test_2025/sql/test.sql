with calendar_dates as (select
    calendar_date
    from unnest(sequence(date({start_date}),date({end_date}),interval '1' day)) as cte (calendar_date)
    where true
)

select * from calendar_dates
