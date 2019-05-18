"""Parse nginx log-file in CSV format and calculate 
latency statistics and API endpoints distribution.

Input CSV: 
    source ip; datetime; http method; url ; resp_time; upstream_time; http_code
"""
import sys
import datetime
import argparse
import csv
import statistics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path_to_file', metavar='FILE', help='Path to CSV file for processing')

    args = parser.parse_args()

    print('DEBUG: args are {}'.format(args))
    timings = []
    request_profile = {}

    with open(args.path_to_file) as input_csv:
        reader = csv.reader(input_csv, delimiter=';')
        for i, row in enumerate(reader):
            if i == 0:
                # skip header
                continue

            resp_time = float(row[4])
            timings.append(resp_time)

            url = row[3]
            request_profile.setdefault(url, 0)
            request_profile[url] += 1

    print("Mean response time: {}".format(statistics.mean(timings)))
    print("Median response time: {}".format(statistics.median(timings)))
    print("Request profile: {}".format(request_profile))

if __name__ == "__main__":
    main()
