# Web Performance Metrics Analysis

This project analyzes web performance metrics from a JSONL dataset. It includes data loading, metric computation, aggregation, and visualization.

## Project Structure

- `data_loader.py`: Loads data from a URL
- `pandas_config.py`: Configures Pandas display options
- `task2.py`: Computes web performance metrics
- `task3.py`: Aggregates metrics by edge assignment
- `task5.py`: Visualizes metrics using histograms and box plots
- `requirements.txt`: Lists project dependencies
- `Dockerfile`: Defines the Docker container for running the project

## Dependencies

The project requires Python 3.7+ and the following libraries:
- pandas
- requests
- seaborn
- matplotlib

## Running the Scripts

1. Install the dependencies: `pip install -r requirements.txt`
2. Run the individual tasks: `python task2.py && python task3.py && python task5.py`


## Using Docker

To run the project in a Docker container:

1. Build the Docker image: `docker build -t web-performance-metrics .`
2. Run the Docker container: `docker run -it --rm -v $(pwd)/output:/app/output web-performance-metrics`

This will execute all tasks and save the results in the `output` directory on your host machine.

3. View the results:
   - Check the `output` directory for generated chart images (PNG files) and the summary statistics text file.
   - Open the PNG files with an image viewer to see the visualizations.
   - Open `summary_statistics.txt` with a text editor to view the statistical summary.

Note: The `-v $(pwd)/output:/app/output` option in the docker run command creates a volume that maps the `output` directory in your current working directory to the `/app/output` directory in the container. This allows the container to write files that persist on your host machine.
These changes will allow you to run the analysis in a Docker container and still be able to view the generated charts and statistics. The visualizations and summary will be saved as files in the output directory, which you can access from your host machine.