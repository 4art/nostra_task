import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_loader import DataLoader
from task2 import WebPerformanceMetrics
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import os


class WebPerformanceMetricsVisualizer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def plot_histograms(self) -> None:
        """
        Generates histograms for TTFB, DOM Content Loaded Time, and Page Load Time
        for the entire dataset, using blue for 'test' and red for 'control' in _edge_assignment.
        Includes mean, median, and 75th percentile lines with corresponding legends.
        Displays the plots and saves them as PNG files.
        """
        metrics = ['TTFB', 'DOM_Content_Loaded_Time', 'Page_Load_Time']
        colors = {'test': 'blue', 'control': 'red'}  # Define colors for 'test' and 'control'

        for metric in metrics:
            plt.figure(figsize=(12, 6))
            sns.histplot(data=self.df, x=metric, hue='_edge_assignment', kde=True, element="step",
                         palette=colors)

            # Calculate mean, median, and 75th percentile for each group
            means = self.df.groupby('_edge_assignment')[metric].mean()
            medians = self.df.groupby('_edge_assignment')[metric].median()
            percentiles_75 = self.df.groupby('_edge_assignment')[metric].quantile(0.75)

            # Plot vertical lines for mean, median, and 75th percentile
            for group in ['test', 'control']:
                plt.axvline(x=means[group], color=colors[group], linestyle='--', linewidth=2)
                plt.axvline(x=medians[group], color=colors[group], linestyle='-.', linewidth=2)
                plt.axvline(x=percentiles_75[group], color=colors[group], linestyle=':', linewidth=2)

            plt.title(f'Histogram of {metric} by _edge_assignment')
            plt.xlabel(metric)
            plt.ylabel('Frequency')
            # Create custom legend
            test_patch = mpatches.Patch(color='blue', label='Test Group (Blue) in _edge_assignment')
            control_patch = mpatches.Patch(color='red', label='Control Group (Red) in _edge_assignment')

            # Custom lines for mean, median, and 75th percentile
            mean_line = Line2D([0], [0], color='black', linestyle='--', linewidth=2, label='Mean')
            median_line = Line2D([0], [0], color='black', linestyle='-.', linewidth=2, label='Median')
            percentile_75_line = Line2D([0], [0], color='black', linestyle=':', linewidth=2, label='75th Percentile')

            plt.legend(handles=[test_patch, control_patch, mean_line, median_line, percentile_75_line],
                       title='Parameters')

            plt.savefig(f'output/{metric}_histogram.png')
            plt.show()
            plt.close()

    def plot_boxplots(self, group_by: str) -> None:
        """
        Generates box plots for TTFB, DOM Content Loaded Time, and Page Load Time
        grouped by a specified column. Displays the plots and saves them as PNG files.

        Parameters:
        - group_by: The column name by which to group the data.
        """
        metrics = ['TTFB', 'DOM_Content_Loaded_Time', 'Page_Load_Time']
        for metric in metrics:
            plt.figure(figsize=(12, 6))
            sns.boxplot(x=group_by, y=metric, hue=group_by, data=self.df, palette={'test': 'blue', 'control': 'red'},
                        legend=False)
            plt.title(f'Box Plot of {metric} by {group_by}')
            plt.xlabel(group_by)
            plt.ylabel(metric)
            plt.savefig(f'output/{metric}_boxplot.png')
            plt.show()
            plt.close()

    def summarize_statistics(self) -> None:
        """
        Prints a summary of basic statistics for the key performance metrics.
        Saves the summary to a text file.
        """
        metrics = ['TTFB', 'DOM_Content_Loaded_Time', 'Page_Load_Time']
        summary = self.df[metrics].describe()
        print("Summary Statistics for Performance Metrics:")
        print(summary)

        with open('output/summary_statistics.txt', 'w') as f:
            f.write("Summary Statistics for Performance Metrics:\n")
            f.write(summary.to_string())


def main():
    url = "https://gist.githubusercontent.com/jhiggins-thrillist/6f246cb9b3541e77a0722190e4e96fa5/raw/8cd8d8831ae4fe499cb3c82231fbc74067752e4a/payloads.jsonl"

    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)

    # Create an instance of the DataLoader class and load the data
    data_loader = DataLoader(url)
    df = data_loader.get_dataframe()

    # Create an instance of the WebPerformanceMetrics class
    web_metrics = WebPerformanceMetrics(df)

    # Compute the full metrics (including all relevant columns)
    df_metrics_full = web_metrics.compute_metrics_full()

    # Create an instance of the WebPerformanceMetricsVisualizer class
    visualizer = WebPerformanceMetricsVisualizer(df_metrics_full)

    # Visualize the most relevant information
    visualizer.summarize_statistics()
    visualizer.plot_histograms()
    visualizer.plot_boxplots('_edge_assignment')

    print("Plots have been saved in the 'output' directory.")


if __name__ == "__main__":
    main()
