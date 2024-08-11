import pandas as pd
from data_loader import DataLoader
from pandas_config import PandasConfig


class WebPerformanceMetrics(PandasConfig):
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.df = df
        self._metrics_computed = False

    def _compute_metrics(self):
        """
                Computes key web performance metrics:
                - Time to First Byte (TTFB)
                - DOM Content Loaded Time
                - Page Load Time
        """
        if not self._metrics_computed:
            self.df['TTFB'] = self.df['responseStart'] - self.df['navigationStart']
            self.df['DOM_Content_Loaded_Time'] = self.df['domContentLoadedEventEnd'] - self.df[
                'domContentLoadedEventStart']
            self.df['Page_Load_Time'] = self.df['loadEventEnd'] - self.df['navigationStart']
            self._metrics_computed = True

    def compute_metrics(self) -> pd.DataFrame:
        """
        Returns
        a
        DataFrame
        with these metrics and '_edge_assignment'.
        """
        self._compute_metrics()
        return self.df[['TTFB', 'DOM_Content_Loaded_Time', 'Page_Load_Time', '_edge_assignment']]

    def compute_metrics_full(self) -> pd.DataFrame:
        """
        Computes key web performance metrics and returns the full DataFrame.

        Returns the entire DataFrame including all original columns and computed metrics.
        """
        self._compute_metrics()
        return self.df


def main():
    url = "https://gist.githubusercontent.com/jhiggins-thrillist/6f246cb9b3541e77a0722190e4e96fa5/raw/8cd8d8831ae4fe499cb3c82231fbc74067752e4a/payloads.jsonl"

    # Config pd
    PandasConfig().apply_config()

    # Create an instance of the DataLoader class and load the data
    data_loader = DataLoader(url)
    df = data_loader.get_dataframe()

    # Create an instance of the WebPerformanceMetrics class
    web_metrics = WebPerformanceMetrics(df)

    # Compute the metrics
    computed_metrics = web_metrics.compute_metrics()
    print("Computed Metrics:")
    print(computed_metrics.head())


if __name__ == "__main__":
    main()
