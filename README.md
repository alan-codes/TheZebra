
# Aggregation

The applicaiton aggregates daily insurance information in csv format into a single output csv file.

The code was developed with Python 2.7 using standard libraries that follow pep8 guidelines. Additonal python libraries such as pandas and numpy can also be used to develop this application but these require pip install.

## How to Run

To run in the application. Run in the following command in the top level of this git directory:
>`python aggregator.py`

## Input - Daily CSV files
The application reads all csv files in the `TheZebra/files` directory. Additional csv files should be added to this directory.

## Output - Aggregate Data and Logs
This application creates two subdirectories -
 - aggregation
 - logs

The aggregation directory contains the aggregated data of the all the daily partner csv files.
The logs directory contains logs for each aggregation output file.

Both files are organised by timestamp values using timestamp format.

## Testing
To run in the unit tests for the application. Run in the following command in the top level of this git directory:
> `python -m unittest testAggregator`
