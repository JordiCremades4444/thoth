with calendar_dates as (select
    calendar_date
    from unnest(sequence(date({start_date}),date({end_date}),interval '1' day)) as cte (calendar_date)
    where true
)

,stores as (
    select distinct
        sa.store_address_id,
        sa.store_id,
        case
            when s.store_subvertical2 in ('Food - Food', 'Food - Other') then 'Food'
            when s.store_subvertical2 in ('Groceries') then 'Groceries'
            when s.store_subvertical2 in ('Retail') then 'Retail'
            else 'Untagged'
        end as vertical
    from delta.partner_stores_odp.store_addresses_v2 sa
    left join delta.partner_stores_odp.stores_v2 s
        on sa.store_id = s.store_id
    where true
        and sa.p_end_date is null
        and s.p_end_date is null
)

,custom_event as (
    select
        cu.creation_date,
        coalesce(s.vertical, 'Not_found') as vertical,
        count(distinct cu.event_id) as n_events,
        count(distinct cu.dynamic_session_id) as n_sessions
    from sensitive_delta.customer_mpcustomer_odp.custom_event cu
    left join stores s
        on cast(cu.custom_attributes__store_address_id as bigint) = s.store_address_id
    where true
        and creation_date in (select calendar_date from calendar_dates)
        and cu.event_name = 'Collection Opened'
        and custom_attributes__collection_type = 'Catalogue'
    group by 1,2
    order by 1,2
)

select * from custom_event
