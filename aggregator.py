#! /usr/bin/python

import csv
import logging
import os
import time

INPUT_DIR = "files"
OUTPUT_DIR = "aggregated_data"
LOG_DIR = "logs"
FIELDS = ["Provider Name", "CampaignID", "Cost Per Ad Click", "Redirect Link",
          "Phone Number", "Address", "Zipcode"]

def setup_logging_and_subdirs():
    ''' Setup subdirectories for output and log if they don't exist'''
    try:
        os.mkdir(OUTPUT_DIR)
    except Exception:
        pass

    try:
        os.mkdir(LOG_DIR)
    except Exception:
        pass

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    output_file = "Aggregation_{}.csv".format(timestamp)

    # Setup log output to stderr and file
    log_file = "{}.log".format(timestamp)
    log_format = "%(levelname)s: %(message)s"
    logging.basicConfig(filename=os.path.join(LOG_DIR, log_file),
                        format=log_format,
                        level=logging.INFO)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(log_format)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    return output_file, logging

def validate_headers(headers, csvfile, logging):
    ''' Validates csv file and headers'''
    valid = True
    try:
        if not set(FIELDS).issubset(headers):
            valid = False
            logging.error("Ignoring {} - missing headers".format(csvfile))
    except Exception as e:
        logging.error("Ignoring {} - unrecognized csv".format(
                      csvfile))
        valid = False

    return valid

def validate_data(row, count, file, logging):
    ''' Validates data for fields to enter into aggregated file '''
    invalid_fields = []
    output_write = True

    for field in FIELDS:

        # Check if fields are empty
        if not row[field]:
            # Phone Number field can be empty/null
            if field == "Phone Number":
                continue
            output_write = False
            invalid_fields.append(field)
            #TODO: update to continue for complete list of invalidities in row.
            break

        # Update data with appropriate type
        row[field] = row[field].strip('"')
        if field == "Cost Per Ad Click":
            try:
                row[field] = float(row[field])
            except Exception as e:
                invalid_fields.append(field)
                output_write = False

    if invalid_fields:
        str = ", ".join(invalid_fields)
        logging.warning("Skipping: missing/invalid values in [{0}] "
                        "for line {1} in file: '{2}'".format(str, count, file))
    return output_write, row

def main():
    ''' Manages reader and writer for aggregated data from daily csv'''
    # Create output/log dirs and files.
    output_file, logging = setup_logging_and_subdirs()

    # Get list of csv files from the data directory
    partner_files = [file
                     for file in os.listdir(INPUT_DIR)
                     if file.endswith('.csv')]

    if not partner_files:
        logging.warn("No daily csv files found in '/{}'".format(INPUT_DIR))
        return

    # Create writer for aggregated file
    aggr_file = open(os.path.join(OUTPUT_DIR, output_file), "w")
    writer = csv.DictWriter(aggr_file, fieldnames=FIELDS,
                quoting=csv.QUOTE_NONE, quotechar='', extrasaction='ignore')
    writer.writeheader()
    logging.info("Created '{}' in /{}".format(output_file, OUTPUT_DIR))

    # Create reader for daily files
    for csvfile in partner_files:
        with open(os.path.join(INPUT_DIR, csvfile), "r") as partner_file:
            reader = csv.DictReader(partner_file)

            # Validate headers
            if not validate_headers(reader.fieldnames, csvfile, logging):
                continue

            # Validate field data and write to file
            line_count = 2 # line 1 is header fields
            for row in reader:
                write, row = validate_data(row, line_count, csvfile, logging)
                if write:
                    writer.writerow(row)
                line_count += 1

    # Close output file
    aggr_file.close()

if __name__ == '__main__':
    main()
