import pandas as pd

from data_loader import DataLoader
from pandas_config import PandasConfig
from task2 import WebPerformanceMetrics


class WebPerformanceMetricsAggregator(PandasConfig):
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.df = df
        self.aggregated_df = None

    def aggregate_metrics(self) -> pd.DataFrame:
        """
        Aggregates the computed metrics by _edge_assignment.
        - Calculates mean, median, and 75th percentile for each metric.

        Returns a DataFrame with aggregated metrics.
        """
        if self.aggregated_df is not None:
            return self.aggregated_df

        # Ensure metrics are computed before aggregation
        web_metrics = WebPerformanceMetrics(self.df)
        self.df = web_metrics.compute_metrics()

        # Define aggregation functions
        aggregation_functions = {
            'TTFB': ['mean', 'median', lambda x: x.quantile(0.75)],
            'DOM_Content_Loaded_Time': ['mean', 'median', lambda x: x.quantile(0.75)],
            'Page_Load_Time': ['mean', 'median', lambda x: x.quantile(0.75)]
        }

        # Rename the lambda function to a proper name for readability
        aggregation_functions_renamed = {
            'TTFB': ['mean', 'median', '75th_percentile'],
            'DOM_Content_Loaded_Time': ['mean', 'median', '75th_percentile'],
            'Page_Load_Time': ['mean', 'median', '75th_percentile']
        }

        # Compute aggregated metrics
        self.aggregated_df = self.df.groupby('_edge_assignment').agg(aggregation_functions)

        # Flatten the multi-level columns
        self.aggregated_df.columns = [
            f'{metric}_{agg_func}'
            for metric, agg_funcs in aggregation_functions_renamed.items()
            for agg_func in agg_funcs
        ]

        # Keep '_edge_assignment' as index instead of resetting it for task5
        return self.aggregated_df

    def get_aggregated_metrics(self) -> pd.DataFrame:
        """
        Returns the aggregated metrics. If not already computed, computes them first.
        """
        if self.aggregated_df is None:
            self.aggregate_metrics()
        return self.aggregated_df


def main():
    url = "https://gist.githubusercontent.com/jhiggins-thrillist/6f246cb9b3541e77a0722190e4e96fa5/raw/8cd8d8831ae4fe499cb3c82231fbc74067752e4a/payloads.jsonl"

    # Create an instance of the DataLoader class and load the data
    data_loader = DataLoader(url)
    df = data_loader.get_dataframe()

    # Create an instance of the WebPerformanceMetricsAggregator class
    aggregator = WebPerformanceMetricsAggregator(df)

    # Aggregate the metrics
    aggregated_metrics = aggregator.aggregate_metrics()
    print("Aggregated Metrics by _edge_assignment:")
    print(aggregated_metrics)


if __name__ == "__main__":
    main()
