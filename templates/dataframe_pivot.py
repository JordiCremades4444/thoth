# Create an instance of DataFramePivot
dp = dataframe_pivot.DataFramePivot(df)

TIME = "XXX"
DIMENSIONS = ["XXX", "XXX"]
MEASURES = ["XXX", "XXX"]
AFFUNCS = ["sum", "mean"]

# Call the pivot_and_aggregate method
p = dp.pivot_and_aggregate(
    t=TIME, dimensions=DIMENSIONS, measures=MEASURES, aggfuncs=AFFUNCS
)

p.head()
