## =====================================
## Query
## =====================================

QUERY_NAME = "XXX.sql"
START_DATE = "'2025-01-01'"
END_DATE = "'2026-01-01'"

params = {"start_date": str(START_DATE), "end_date": str(END_DATE)}

df = q.run_query_starburst(  # or run_table_explorer_bigquery
    QUERY_NAME, params=params, csv_file=QUERY_NAME, load_csv_file=False
)

df.head()

## =====================================
## Explore Table
## =====================================

TABLE = "delta.central_order_descriptors_odp.order_descriptors_v2"

df = q.run_table_explorer_starburst(TABLE)  # or run_table_explorer_bigquery
