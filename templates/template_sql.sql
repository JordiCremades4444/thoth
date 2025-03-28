-- =====================================
-- Calendar dates
-- =====================================

with calendar_dates as (select
    calendar_date
    from unnest(sequence(date({start_date}),date({end_date}),interval '1' day)) as cte (calendar_date)
    where true
)

-- =====================================
-- Starburst
-- =====================================

delta.central__retention_orders__odp.retention_order_info
delta.central_geography_odp.cities_v2
delta.central_order_descriptors_odp.order_descriptors_v2
delta.central_users_odp.users_v2
delta.customer__funwithflags_experiment_assignments_daily__odp.funwithflags_experiment_assignments_daily
delta.customer_behaviour_odp.enriched_custom_event__category_group_opened_v3
delta.customer_behaviour_odp.enriched_custom_event__category_opened_v3
delta.customer_behaviour_odp.enriched_custom_event__order_created_v3
delta.customer_behaviour_odp.enriched_custom_event__store_accessed_v3
delta.customer_behaviour_odp.enriched_screen_view__home_v3
delta.customer_behaviour_odp.enriched_screen_view__stores_v3
delta.customer_bought_products_odp.bought_products_v2
delta.mfc__groceries_content_availability_targets__odp.groceries_top_partners
delta.mfc__pna__odp.pna_orders_info
delta.mfc__pna__odp.pna_products_info
delta.mfc__pna_replacement_instructions__odp.pna_replacement_instructions
delta.mfc__groceries_content_availability_targets__odp.groceries_top_partners
delta.mlp__experiment_first_exposure__odp.first_exposure
delta.partner_stores_odp.store_addresses_v2
delta.partner_stores_odp.stores_v2
delta.tech__partner_order_analytics_order_dispatched_with_pna_v0__odp.partner_orders_orderdispatchedtopartnerwithpnaanalyticsevent
delta.tech__shopping_core_gifting_analytics_order_gifting_v0__odp.shoppingcore_gifting_ordergiftingcreatedevent
sensitive_delta.customer_mpcustomer_odp.custom_event


-- =====================================
-- BigQuery
-- =====================================
fulfillment-dwh-production.curated_data_shared_experimentation.experiment_assignment_glovo
