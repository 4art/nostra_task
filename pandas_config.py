import pandas as pd

class PandasConfig:
    def __init__(self, max_columns: int = 10, max_rows: int = 10):
        self.max_columns = max_columns
        self.max_rows = max_rows
        self.apply_config()

    def apply_config(self) -> None:
        """
        Applies the Pandas display configuration.
        Sets the maximum number of rows and columns to display.
        """
        pd.set_option('display.max_columns', self.max_columns)
        pd.set_option('display.max_rows', self.max_rows)

