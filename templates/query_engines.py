QUERY_NAME = "XXX.sql"  # With sql
START_DATE = "'YYYY-MM-DD'"
END_DATE = "'YYYY-MM-DD'"

params = [
    {"name": "start_date", "value": str(START_DATE)},
    {"name": "end_date", "value": str(END_DATE)},
]

q.prepare_query(QUERY_NAME, params=params, output_file=QUERY_NAME, load_previous=False)

df = q.query_run_starburst()
df.head()
