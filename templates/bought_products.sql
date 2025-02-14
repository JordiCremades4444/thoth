,bought_products as (
    select
        bought_product_id,
        product_id,
        order_id,
        store_address_id,
        product_external_id,
        product_name,
        product_weight_in_kg,
        product_unit_price,
        bought_product_quantity,
        product_category,
        replaced_bought_product_id,
        product_brand,
        product_is_deleted,
        replaced_by_bought_product_id,
        product_is_alcoholic,
        product_is_tobacco,
        collection_section_name,
        collection_name,
        collection_group_name,
        bought_product_created_at,
        bought_product_updated_at,
        p_creation_date,
        store_product_id
    from delta.customer_bought_products_odp.bought_products_v2
    where true
)
