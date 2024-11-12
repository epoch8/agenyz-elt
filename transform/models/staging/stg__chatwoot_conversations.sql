{{
    config(
        tags=['staging'],
        materialized = 'incremental',
        incremental_strategy = 'merge',
        unique_key = 'id',
        partition_by = {
            "field": "updated_at",
            "data_type": "timestamp",
            "granularity": "day"
        },
        cluster_by = 'id'
    )
}}

with t1 as (
    select
        *
    from {{source('raw__chatwoot', 'conversations')}}

    {% if is_incremental() %}
        where date(updated_at) >= (
            select max(date(updated_at)) - interval '6 days' from {{ this }} as this
        )
    {% endif %}
)
select * from t1