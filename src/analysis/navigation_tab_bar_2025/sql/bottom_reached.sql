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

,collection_opened as (
    select
        creation_date,
        count(distinct event_id) as n_events
    from sensitive_delta.customer_mpcustomer_odp.custom_event cu
    where true
        and creation_date in (select calendar_date from calendar_dates)
        and cu.event_name = 'Collection Opened'
        and cu.custom_attributes__collection_type = 'Catalogue'
        and cu.custom_attributes__store_address_id in (select cast(store_address_id as varchar) from groceries_stores_filtered)
    group by 1
)

,bottom_reached as (
    select
        creation_date,
        count(distinct event_id) as n_events
    from sensitive_delta.customer_mpcustomer_odp.custom_event cu
    where true
        and cu.creation_date in (select calendar_date from calendar_dates)
        and cu.event_name = 'Screen Bottom Reached'
        and custom_attributes__collection_type = 'Catalogue'
        and cu.custom_attributes__store_address_id in (select cast(store_address_id as varchar) from groceries_stores_filtered)
    group by 1
)

select
    co.creation_date,
    co.n_events as n_collection_opened,
    br.n_events as n_bottom_reached
from collection_opened co
left join bottom_reached br
    on co.creation_date = br.creation_date
where true
