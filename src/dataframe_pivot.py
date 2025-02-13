import pandas as pd


class DataFramePivot:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def pivot_and_aggregate(
        self, t: str, dimensions: list, measures: list, aggfuncs: list = ["sum"]
    ):
        """
        Pivots and aggregates the DataFrame.

        Parameters:
            t (str): The time column in the DataFrame.
            dimensions (list): List of dimension columns to pivot.
            measures (list): List of measure columns to aggregate.
            aggfuncs (list, optional): List of aggregation functions to use
                                       (default is ['sum']).

        Returns:
            pd.DataFrame: Pivoted and aggregated DataFrame.
        """
        # Create a dictionary for aggregation functions
        agg_dict = {measure: aggfuncs for measure in measures}

        # Create a pivot table
        pivot_table = pd.pivot_table(
            self.df, values=measures, index=[t], columns=dimensions, aggfunc=agg_dict
        )

        # Flatten the multi-index columns
        pivot_table.columns = [
            "_".join(map(str, col)).strip() for col in pivot_table.columns.values
        ]
        pivot_table.reset_index(inplace=True)

        return pivot_table
