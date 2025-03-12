with calendar_dates as (select
    calendar_date
    from unnest(sequence(date({start_date}),date({end_date}),interval '1' day)) as cte (calendar_date)
    where true
)

-- =====================================
-- Stores
-- =====================================

,target_stores as (
    select distinct
        c.country_code,
        s.store_name,
        s.store_id,
        1 as is_target,
        0 as rank
    from delta.partner_stores_odp.stores_v2 s
    left join delta.central_geography_odp.cities_v2 c
        on s.city_code = c.city_code
    where true
        and s.p_end_date is null
        and s.store_subvertical = 'QCPartners'
        and s.store_subvertical2 = 'Groceries'
        and (
            c.country_code = {country}
            and {name_condition}

        )
)

,orders_synthetic_control as (
    select
        od.store_name,
        count(distinct od.order_id) as orders
    from delta.central_order_descriptors_odp.order_descriptors_v2 od
    inner join calendar_dates
        on od.p_creation_date = calendar_dates.calendar_date
    where true
        and od.order_subvertical = 'QCPartners'
        and od.order_subvertical2 = 'Groceries'
        and od.order_country_code = {country}
        and od.store_id not in (select store_id from target_stores)
    group by 1
)

,store_orders_ranked as (
    select
        store_name,
        orders,
        rank() over (order by orders desc) as order_rank
    from orders_synthetic_control
    order by 3 asc
    limit {synthetic_group}
)

,synthetic_group_stores as (
    select distinct
        c.country_code,
        s.store_name,
        s.store_id,
        0 as is_target,
        order_rank as rank
    from delta.partner_stores_odp.stores_v2 s
    left join delta.central_geography_odp.cities_v2 c
        on s.city_code = c.city_code
    inner join store_orders_ranked
        on s.store_name = store_orders_ranked.store_name
    where true
        and s.p_end_date is null
        and s.store_subvertical = 'QCPartners'
        and s.store_subvertical2 = 'Groceries'
        and (
            c.country_code = {country}
            and s.store_name in (select store_name from store_orders_ranked)
        )
)

,all_stores as (
    select
        *
    from target_stores
    union all
    select
        *
    from synthetic_group_stores
    where true
)

-- =====================================
-- Product funnel
-- =====================================

,store_impressions as (
    select distinct
        p_creation_date,
        dynamic_session_id,
        store_id
    from delta.customer_behaviour_odp.enriched_custom_event__store_impression_v3
    inner join calendar_dates
        on p_creation_date = calendar_date
    where true
        and country = {country}
        and store_id in (select store_id from all_stores)
)

,store_accessed as (
    select distinct
        p_creation_date,
        dynamic_session_id,
        store_id
    from delta.customer_behaviour_odp.enriched_custom_event__store_accessed_v3 sa
    inner join calendar_dates
        on sa.p_creation_date = calendar_dates.calendar_date
    where true
        and country = {country}
        and store_id in (select store_id from all_stores)
)

,orders_created as (
    select distinct
        p_creation_date,
        dynamic_session_id,
        store_id
    from delta.customer_behaviour_odp.enriched_custom_event__order_created_v3 oc
    inner join calendar_dates
        on p_creation_date = calendar_date
    where true
        and country = {country}
        and store_id in (select store_id from all_stores)
)

,funnel as (
    select
        si.p_creation_date,
        s.store_name,
        s.is_target,
        s.rank,
        count(distinct si.dynamic_session_id) as impressions,
        count(distinct sa.dynamic_session_id) as accessed,
        count(distinct oc.dynamic_session_id) as orders,
        1.00*count(distinct sa.dynamic_session_id)/nullif(count(distinct si.dynamic_session_id),0) as ctr,
        1.00*count(distinct oc.dynamic_session_id)/nullif(count(distinct si.dynamic_session_id), 0) as cvr
    from store_impressions si
    left join store_accessed sa
        on si.p_creation_date = sa.p_creation_date
        and si.dynamic_session_id = sa.dynamic_session_id
        and si.store_id = sa.store_id
    left join orders_created oc
        on si.p_creation_date = oc.p_creation_date
        and si.dynamic_session_id = oc.dynamic_session_id
        and si.store_id = oc.store_id
    left join all_stores s
        on si.store_id = s.store_id
    where true
    group by 1,2,3,4
)

select * from funnel
