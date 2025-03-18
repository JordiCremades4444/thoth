with calendar_dates as (select
    calendar_date
    from unnest(sequence(date({start_date}),date({end_date}),interval '1' day)) as dates (calendar_date)
    where true
)

,groceries_stores as (
    select distinct
        sa.store_address_id,
        sa.store_id,
        case
            when store_subvertical2 in ('Food - Food', 'Food - Other') then 'Food'
            when store_subvertical2 in ('Groceries') then 'Groceries'
            when store_subvertical2 in ('Retail') then 'Retail'
            else null
        end as vertical
    from delta.partner_stores_odp.store_addresses_v2 sa
    left join delta.partner_stores_odp.stores_v2 s
        on sa.store_id = s.store_id
    where true
        and sa.p_end_date is null
        and s.p_end_date is null
        and store_subvertical2 = 'Groceries' -- Filter for Groceries stores
)

,groceries_stores_filtered as ( -- Filter for Groceries stores with more than 2 Super Collections
    select
        store_address_id,
        count(distinct collection_group_name) n_sc
    from delta.partner__product_collections__odp.product_collections
    where true
        and store_address_id in (select store_address_id from groceries_stores)
        and p_snapshot_date = (select max(p_snapshot_date) from delta.partner__product_collections__odp.product_collections)
        and collection_group_name is not null
        and collection_group_name != 'Unknown'
    group by 1
    having count(distinct collection_group_name) > 2
)

,navigation_impression_sessions as (
    select
        creation_date,
        count(distinct cu.dynamic_session_id) as n_sessions
    from sensitive_delta.customer_mpcustomer_odp.custom_event cu
    where true
        and cu.creation_date in (select calendar_date from calendar_dates)
        and cu.event_name = 'Store Mobile Navigation Bar Impression'
        and cu.custom_attributes__store_address_id in (select cast(store_address_id as varchar) from groceries_stores)
    group by 1
)

,navigation_tapped as (
    select
        event_id,
        dynamic_session_id,
        creation_time,
        creation_date,
        coalesce(custom_attributes__collection_id, custom_attributes__collection_group_id) as element_tapped
    from sensitive_delta.customer_mpcustomer_odp.custom_event cu
    where true
        and cu.creation_date in (select calendar_date from calendar_dates)
        and cu.event_name = 'Navigation Bar Element Tapped'
        and (
            (custom_attributes__collection_type = 'Catalogue' and custom_attributes__collection_id is not null) -- Filter for Collection Taps
            or (custom_attributes__collection_group_id is not null) -- Filter for SuperCollection Taps
        )
)

,collection_opened as (
    select distinct
        event_id,
        dynamic_session_id,
        creation_time,
        creation_date,
        custom_attributes__collection_group_id,
        custom_attributes__collection_id,
        custom_attributes__store_address_id as store_address_id
    from sensitive_delta.customer_mpcustomer_odp.custom_event cu
    where true
        and creation_date in (select calendar_date from calendar_dates)
        and cu.custom_attributes__store_address_id in (select cast(store_address_id as varchar) from groceries_stores_filtered) -- Filter for Groceries stores with more than 2 Super Collections
        and cu.event_name = 'Collection Opened'
)

,navigation_tapped_enriched as (
    select distinct
        nt.event_id,
        nt.dynamic_session_id,
        nt.creation_time,
        nt.creation_date,
        co.store_address_id,
        case when nt.element_tapped = co.custom_attributes__collection_id then 'Collection'
             when nt.element_tapped = co.custom_attributes__collection_group_id then 'SuperCollection'
             else 'Other'
        end as element_tapped
    from navigation_tapped nt
    inner join collection_opened co -- We only keep those taps that we can map
        on nt.dynamic_session_id = co.dynamic_session_id
        and co.creation_time between nt.creation_time and nt.creation_time + interval '2' minute
        and (nt.element_tapped = co.custom_attributes__collection_id or nt.element_tapped = co.custom_attributes__collection_group_id) -- To be able to join the two kinds of taps - in collections and supercollections
    where true
)

,navigation_taps as (
    select
        creation_date,
        count(distinct case when element_tapped = 'Collection' then event_id end) as bar_collection_taps_events,
        count(distinct case when element_tapped = 'SuperCollection' then event_id end) as bar_supercollection_taps_events,
        count(distinct event_id) as bar_any_taps_events
    from navigation_tapped_enriched
    group by 1
)

select
    nis.creation_date,
    nis.n_sessions,
    nt.bar_collection_taps_events,
    nt.bar_supercollection_taps_events,
    nt.bar_any_taps_events
from navigation_impression_sessions nis
left join navigation_taps nt
    on nis.creation_date = nt.creation_date
