import pandas as pd


class DataframeSyntheticControlPreparation:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def prepare_synthetic_control(self, t: str, target_col: str):
        """
        Prepares the DataFrame for synthetic control analysis.

        Parameters:
            t (str): The time column in the DataFrame.
            target_col (str): The target column to be renamed as 'y'.

        Returns:
            pd.DataFrame: Prepared DataFrame with 'y' as the target column and
                          other columns renamed as 'x1', 'x2', 'x3', etc.
            tuple: A tuple containing the prepared DataFrame and a list of tuples
                   with the original and final names of each column.
        """
        # Set the time column as index
        self.df[t] = pd.to_datetime(self.df[t])
        self.df.set_index(t, inplace=True)

        # Rename the target column to 'y'
        self.df.rename(columns={target_col: "y"}, inplace=True)

        # Rename the rest of the columns to 'x1', 'x2', 'x3', etc.
        other_cols = [col for col in self.df.columns if col != "y"]
        new_col_names = {col: f"x{i+1}" for i, col in enumerate(other_cols)}
        self.df.rename(columns=new_col_names, inplace=True)

        # Reorder the columns to have 'y' first, followed by 'x1', 'x2', 'x3', etc.
        ordered_cols = ["y"] + [f"x{i+1}" for i in range(len(other_cols))]
        self.df = self.df[ordered_cols]

        # Create a list of tuples with the original and final names of each column
        column_mapping = [(target_col, "y")] + [
            (col, new_col_names[col]) for col in other_cols
        ]

        return self.df, column_mapping
