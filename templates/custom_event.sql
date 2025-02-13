,custom_event as (
    select
        cu.creation_date,
        cu.creation_time,
        cu.dynamic_session_id,
        cu.event_id,
        cu.custom_attributes__store_address_id,
        cu.custom_attributes__store_id
    from sensitive_delta.customer_mpcustomer_odp.custom_event cu
    inner join calendar_dates cd
        on cd.calendar_date = cu.creation_date
    where true
        and cu.event_name = XXX
)

-- https://openmetadata.g8s-data-platform-prod.glovoint.com/table/Starburst%20Prod%20Sensitive%20Delta.sensitive_delta.customer_mpcustomer_odp.custom_event
