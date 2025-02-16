-- =====================================
-- Stores
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
        --and contains(et.store_tags, 'Pharmacy OTC')
)
