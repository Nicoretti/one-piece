#!/usr/bin/env python3
import sys
import csv
import datetime
import argparse


def create_parser():
    p = argparse.ArgumentParser("hm-importer", argument_default=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('csv', type=argparse.FileType('r'), default=sys.stdin)
    p.add_argument('--date-format', choices=['d/m/y', 'm/d/y'], default='d/m/y')
    return p


def breuer_hm_csv_entries(csv_file, date_fmt):
    # skip unrelevant data (User data etc)
    while not (line := csv_file.readline()).strip().startswith('WEIGHT'):
        pass

    reader = csv.DictReader(csv_file, delimiter=';')
    for entry in reader:
        parts = entry['Date'].split('/')
        parts = parts[2], parts[1], parts[0] if date_fmt == 'd/m/y' else parts[2], parts[0], parts[1]
        date = '{}-{}-{}'.format(*parts)
        entry['Date'] = datetime.date.fromisoformat(date)
        # TODO: Detect and convert time
        entry['Weight'] = float(entry['Weight'])
        entry['Body fat'] = float(entry['Body fat'])
        entry['Water'] = float(entry['Water'])
        entry['Muscles'] = float(entry['Muscles'])
        entry['Bones'] = float(entry['Bones'])
        entry['BMR'] = int(entry['BMR'])
        entry['AMR'] = int(entry['AMR'])
        yield entry


def main(argv=None):
    parser = create_parser()
    args = parser.parse_args(argv)
    sys.exit(-1)


if __name__ == '__main__':
    main()
