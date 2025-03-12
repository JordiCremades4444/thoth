-- =====================================
-- Calendar dates
-- =====================================

with calendar_dates as (select
    calendar_date
    from unnest(sequence(date({XXX}),date({XXX}),interval '1' day)) as cte (calendar_date)
    where true
)

-- =====================================
-- Custom event
-- =====================================

,custom_event as (
    select
        cu.creation_date,
        cu.creation_time,
        cu.dynamic_session_id,
        cu.event_id,
        cu.custom_attributes__store_address_id
    from sensitive_delta.customer_mpcustomer_odp.custom_event cu
    inner join calendar_dates cd
        on cd.calendar_date = cu.creation_date
    where true
        and cu.event_name = XXX
)

-- =====================================
-- Order level
-- =====================================

,orders as (
    select
        od.p_creation_date,
        od.order_id
    from delta.central_order_descriptors_odp.order_descriptors_v2 od
    inner join calendar_dates
        on od.p_creation_date = calendar_dates.calendar_date
    where true
)

-- Careful orders appear more than once in the table
,orders_with_pna_instructions as (
    select distinct
        oi.p_ingestion_date as p_creation_date,
        oi.orderid as order_id,
        products as instrucions
    from delta.tech__partner_order_analytics_order_dispatched_with_pna_v0__odp.partner_orders_orderdispatchedtopartnerwithpnaanalyticsevent oi
    inner join calendar_dates
        on oi.p_ingestion_date = calendar_dates.calendar_date
    where true
)

-- I've not seen duplicated orders in the table, but be careful
,gifting_orders_with_instructions as (
    select distinct
        go.p_ingestion_date as p_creation_date,
        orderid as go.order_id,
        giftreceiptrequested,
        giftmessagerequested
    from delta.tech__shopping_core_gifting_analytics_order_gifting_v0__odp.shoppingcore_gifting_ordergiftingcreatedevent go
    inner join calendar_dates
        on go.p_ingestion_date = calendar_dates.calendar_date
    where true
)

,pna_orders_info as (
    select
        poi.p_creation_date,
        poi.order_id
    from delta.mfc__pna__odp.pna_orders_info poi
    inner join calendar_dates
        on poi.p_creation_date = calendar_dates.calendar_date
    where true
)

,retention_orders_info as (
    select
        roi.p_creation_date,
        roi.order_id
    from delta.central__retention_orders__odp.retention_order_info roi
    inner join calendar_dates
        on roi.p_creation_date = calendar_dates.calendar_date
    where true
)

-- =====================================
-- Product funnel
-- =====================================

,map_category_opened as ( -- cateogy end possibilities are Food, Health, Groceries, Shops, Smoking and Specialties
    select distinct
        co.p_creation_date,
        co.country,
        co.category_id,
        case when co.category_sub_tag in ('Smoking', 'Specialties') then co.category_sub_tag else co.category_tag end as category
    from delta.customer_behaviour_odp.enriched_custom_event__category_opened_v3 co
    inner join calendar_dates cd
        on cd.calendar_date = co.p_creation_date
    where true
        and co.category_tag in ('Food', 'Health', 'Groceries', 'Shops')
)

,map_category_group_opened as (-- category end possibilities are Food, Health, Groceries, Shops
    select distinct
        gco.p_creation_date,
        gco.country,
        gco.group_id,
        gco.category_tag as category
    from delta.customer_behaviour_odp.enriched_custom_event__category_group_opened_v3 gco
    inner join calendar_dates cd
        on cd.calendar_date = gco.p_creation_date
    where true
        and gco.category_tag in ('Food', 'Health', 'Groceries', 'Shops')
)

,homes as (
    select
        h.p_creation_date,
        h.creation_time,
        h.dynamic_session_id,
        h.event_id
    from delta.customer_behaviour_odp.enriched_screen_view__home_v3 h
    inner join calendar_dates
        on h.p_creation_date = calendar_dates.calendar_date
    where true
)

,group_category_opened as (
    select
        gco.p_creation_date,
        gco.creation_time,
        gco.dynamic_session_id,
        gco.event_id
    from delta.customer_behaviour_odp.enriched_custom_event__category_group_opened_v3 gco
    inner join calendar_dates
        on gco.p_creation_date = calendar_dates.calendar_date
    where true
)

,category_opened as (
    select
        co.p_creation_date,
        co.creation_time,
        co.dynamic_session_id,
        co.event_id
    from delta.customer_behaviour_odp.enriched_custom_event__category_opened_v3 co
    inner join calendar_dates
        on co.p_creation_date = calendar_dates.calendar_date
    where true
)

,store_wall_events AS (
    select
        sw.p_creation_date,
        sw.creation_time,
        sw.dynamic_session_id,
        sw.event_id,
        coalesce(mco.category, mcgo.category) as category
    from delta.customer_behaviour_odp.enriched_screen_view__stores_v3 sw
    inner join calendar_dates
        on sw.p_creation_date = calendar_dates.calendar_date
    left join map_category_opened mco
        on sw.category_id = mco.category_id
        and sw.p_creation_date = mco.p_creation_date
        and sw.country = mco.country
    left join map_category_group_opened mcgo
        on sw.category_group_id = mcgo.group_id
        and sw.p_creation_date = mcgo.p_creation_date
        and sw.country = mcgo.country
    where true
)

,store_accessed as (
    select
        sa.p_creation_date,
        sa.creation_time,
        sa.dynamic_session_id,
        sa.event_id
    from delta.customer_behaviour_odp.enriched_custom_event__store_accessed_v3 sa
    inner join calendar_dates
        on sa.p_creation_date = calendar_dates.calendar_date
    where true
)

,orders_created as (
    select
        oc.p_creation_date,
        oc.creation_time,
        oc.dynamic_session_id,
        oc.event_id,
        s.category --category of the order
    from delta.customer_behaviour_odp.enriched_custom_event__order_created_v3 oc
    inner join calendar_dates
        on oc.p_creation_date = calendar_dates.calendar_date
    inner join stores s -- category of the order
        on oc.store_id = s.store_id
    where true
)

select
    sw.p_creation_date,
    sw.category,
    ce.variant,
    count(distinct sw.dynamic_session_id) as n_sessions_sw,
    count(distinct oc.dynamic_session_id) as n_sessions_orders
from store_wall_events sw
left join customer_exposure ce
    on sw.customer_id = ce.customer_id
    and sw.p_creation_date between ce.start_time and ce.end_time
left join orders_created oc
    on oc.p_creation_date = sw.p_creation_date
    and oc.dynamic_session_id = sw.dynamic_session_id
    and oc.creation_time >= sw.creation_time
    and oc.category = sw.category
where true
group by 1,2,3

-- =====================================
-- Product level
-- =====================================

,bought_products as (
    select
        bp.p_creation_date,
        bp.bought_product_id
    from delta.customer_bought_products_odp.bought_products_v2 bp
    inner join calendar_dates
        on bp.p_creation_date = calendar_dates.calendar_date
    where true
)

,pna_products_info as (
    select
        ppi.p_creation_date,
        ppi.bought_product_id
    from delta.mfc__pna__odp.pna_products_info ppi
    inner join calendar_dates
        on ppi.p_creation_date = calendar_dates.calendar_date
    where true
)

,products_with_pna_instructions as (
    select
        pri.bought_product_id,
        pri.order_id,
        pri.instrucion,
        pri.alternative_products,
        pri.replacer_bought_product_id,
        pri.is_replacer_and_alternative_product,
    from delta.mfc__pna_replacement_instructions__odp.pna_replacement_instructions pri
    inner join calendar_dates
        on pri.p_order_activated_date = calendar_dates.calendar_date -- p_order_activated_date is the date when the order was activated
    where true
)

-- =====================================
-- User classification
-- =====================================

with calendar_dates as (select
    calendar_date
    from unnest(sequence(date({start_date}),date({end_date}),interval '1' day)) as dates (calendar_date)
    where true
)

,glovo_customers as (
    select
        u.user_id as customer_id
    from delta.central_users_odp.users_v2 u
    where true
        and not user_is_staff
        and not user_is_glovo_employee
        and user_type = 'Customer'
)

,customer_exposure as (
    select distinct
        fe.allocation_key as customer_id
        ,fe.variant
        ,fe.first_exposure_datetime as start_time
        ,coalesce(lag(fe.first_exposure_datetime) over (partition by fe.allocation_key order by fe.first_exposure_datetime desc), current_timestamp) as end_time -- fe.first_exposure_datetime because they could be in the same day
    from delta.mlp__experiment_first_exposure__odp.first_exposure fe
    inner join calendar_dates cd
        on cd.calendar_date = fe.p_first_exposure_date
    where true
        and fe.allocation_key in (select customer_id from glovo_customers)
        and fe.experiment_toggle_id = XXX
)

-- =====================================
-- Stores & Top Partners
-- =====================================

,stores as (
    select distinct
        sa.store_address_id,
        sa.store_id
    from delta.partner_stores_odp.store_addresses_v2 sa
    left join delta.partner_stores_odp.stores_v2 s
        on sa.store_id = s.store_id
    left join delta.partner_stores_odp.store_entity_tags et
        on sa.store_id = et.store_id
    left join delta.central_geography_odp.cities_v2 c
        on s.city_code = c.city_code
    where true
        and sa.p_end_date is null
        and s.p_end_date is null
        and et.p_end_date is null
        and s.store_vertical = XXX -- QCommerce, Food
        and s.store_subvertical = XXX -- QCPartners, MFC, Food - Other, Food - Food
        and s.store_subvertical2 = XXX -- Food - Food, Food - Other, Retail, Groceries
        and s.store_subvertical3 = XXX -- Food - Food, Food - Other, Smoking, Health, Retail, Shops
        and contains(et.store_tags, 'Pharmacy OTC')
)

,top_groceries_partners as (
    select distinct
        country_code,
        store_name
    from delta.mfc__groceries_content_availability_targets__odp.groceries_top_partners
    where true
        and p_ingestion_date = (select max(p_ingestion_date) from delta.mfc__groceries_content_availability_targets__odp.groceries_top_partners)
)
