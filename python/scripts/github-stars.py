#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///

# GitHub Stars Downloader
import sys
import requests
import json
import argparse
import time


def fetch_stars(username, rate_limit):
    page = 1
    per_page = 100
    headers = {}

    while True:
        url = f"https://api.github.com/users/{username}/starred?page={page}&per_page={per_page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error: {response.status_code}", file=sys.stderr)
            print(response.json(), file=sys.stderr)
            break

        stars = response.json()
        for star in stars:
            yield star

        if not stars:
            break

        page += 1
        time.sleep(rate_limit)


def to_jsonl(stars):
    for star in stars:
        json_star = {
            'id': star['id'],
            'name': star['name'],
            'full_name': star['full_name'],
            'html_url': star['html_url'],
            'description': star['description'],
            'homepage': star['homepage'],
            'language': star['language'],
            'license': star['license'],
            'topics': star.get('topics', []),
        }
        yield json.dumps(json_star)


def _create_parser():
    parser = argparse.ArgumentParser(
        description='Download all GitHub stars for a user',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('username', help='GitHub username')
    parser.add_argument(
        '-r', '--rate-limit', type=float,
        default=0.2, help='Seconds to wait between requests'
    )
    return parser


def main():
    parser = _create_parser()
    args = parser.parse_args()

    stars = fetch_stars(args.username, args.rate_limit)
    stars = to_jsonl(stars)
    for star in stars:
        print(star)

    sys.exit(0)


if __name__ == "__main__":
    main()
