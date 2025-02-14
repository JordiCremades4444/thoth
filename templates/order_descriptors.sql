,order_descriptors_v2 as (
    select
        order_id,
        customer_id,
        courier_id,
        store_id,
        store_address_id,
        store_category_id,
        store_name,
        order_parent_id,
        order_parent_relationship_type,
        order_code,
        order_final_status,
        order_cancel_reason,
        order_cancel_comments,
        order_vertical,
        order_subvertical,
        order_subvertical2,
        order_subvertical3,
        order_subtype,
        order_handling_strategy,
        order_courier_payment_method,
        order_courier_provider,
        order_is_partner_order,
        order_is_first_created_order,
        order_is_first_delivered_order,
        order_number_of_assignments,
        device_id,
        order_customer_device_operating_system,
        order_partner_commission_pct,
        order_is_prime,
        order_is_discounted,
        order_pricing_id,
        order_total_purchase_local,
        order_total_purchase_eur,
        order_total_effective_purchase_local,
        order_total_effective_purchase_eur,
        order_balance_discount_local,
        order_balance_discount_eur,
        order_estimated_purchase_local,
        order_estimated_purchase_eur,
        order_cancellation_fee_local,
        order_cancellation_fee_eur,
        order_delivery_fee_local,
        order_delivery_fee_eur,
        order_service_fee_local,
        order_service_fee_eur,
        order_effective_weather_surcharge_local,
        order_effective_weather_surcharge_eur,
        order_weather_surcharge_local,
        order_weather_surcharge_eur,
        order_effective_min_basket_surcharge_local,
        order_effective_min_basket_surcharge_eur,
        order_initial_delivery_fee_local,
        order_initial_delivery_fee_eur,
        order_tax_rate,
        order_gen1_commission_flat_fee_local,
        order_gen1_commission_flat_fee_eur,
        order_transacted_value_local,
        order_transacted_value_eur,
        order_arrears_local,
        order_arrears_eur,
        order_timezone,
        order_created_at,
        order_updated_at,
        order_scheduled_at,
        order_activated_at,
        order_started_at,
        order_dispatched_at,
        order_accepted_by_partner_at,
        order_courier_arrival_to_pickup_at,
        order_courier_arrival_to_delivery_at,
        order_picked_up_by_courier_at,
        order_terminated_at,
        order_created_local_at,
        order_updated_local_at,
        order_scheduled_local_at,
        order_activated_local_at,
        order_started_local_at,
        order_dispatched_local_at,
        order_accepted_by_partner_local_at,
        order_courier_arrival_to_pickup_local_at,
        order_courier_arrival_to_delivery_local_at,
        order_picked_up_by_courier_local_at
    from delta.central_order_descriptors_odp.order_descriptors_v2
    where true
)
