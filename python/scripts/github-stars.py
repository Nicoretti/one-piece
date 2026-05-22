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


class GitHubStarredIterator:
    """Custom iterator that handles pagination for GitHub starred repositories."""

    def __init__(self, username, rate_limit=0.2, per_page=100):
        self.username = username
        self.rate_limit = rate_limit
        self.per_page = per_page
        self.page = 1
        self.current_items = []
        self.index = 0
        self.headers = {}
        self.exhausted = False

    def __iter__(self):
        return self

    def __next__(self):
        def has_items_in_current_batch(index, current_items):
            """Check if there are more items in the current batch."""
            return index < len(current_items)

        def get_next_item_from_batch(current_items, index):
            """Get the next item from current batch and return it with updated index."""
            item = current_items[index]
            return item, index + 1

        def apply_rate_limit(page, rate_limit):
            """Apply rate limiting if not the first request."""
            if page > 1:
                time.sleep(rate_limit)

        def fetch_page(username, page, per_page, headers, rate_limit):
            """Fetch a page of starred repositories from GitHub API."""
            url = f"https://api.github.com/users/{username}/starred?page={page}&per_page={per_page}"
            apply_rate_limit(page, rate_limit)
            response = requests.get(url, headers=headers)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as ex:
                raise StopIteration from ex

            return response.json()

        # If we have items in current batch, return next item
        if has_items_in_current_batch(self.index, self.current_items):
            item, self.index = get_next_item_from_batch(self.current_items, self.index)
            return item

        # If we've already exhausted the API, stop
        if self.exhausted:
            raise StopIteration

        # Fetch next page
        self.current_items = fetch_page(self.username, self.page, self.per_page, self.headers, self.rate_limit)

        # If no items returned, we're done
        if not self.current_items:
            self.exhausted = True
            raise StopIteration

        # Reset index and increment page for next fetch
        self.index = 0
        self.page += 1

        # Return first item from new batch
        item, self.index = get_next_item_from_batch(self.current_items, self.index)
        return item


def fetch_stars(username, rate_limit):
    """Fetch all starred repositories for a user using custom iterator."""
    return GitHubStarredIterator(username, rate_limit)


def to_jsonl(stars):
    for star in stars:
        json_star = {
            "id": star["id"],
            "name": star["name"],
            "full_name": star["full_name"],
            "html_url": star["html_url"],
            "description": star["description"],
            "homepage": star["homepage"],
            "language": star["language"],
            "license": star["license"],
            "topics": star.get("topics", []),
        }
        yield json.dumps(json_star)

def to_json(stars):
    stars = list(stars)
    yield json.dumps(stars)


def _create_parser():
    parser = argparse.ArgumentParser(
        description="Download all GitHub stars for a user", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("username", help="GitHub username")
    parser.add_argument("-r", "--rate-limit", type=float, default=0.2, help="Seconds to wait between requests")
    parser.add_argument("-f", "--format", choices=('jsonl', 'json'), default='jsonl', help="Output format")
    return parser


def main():
    parser = _create_parser()
    args = parser.parse_args()
    stars = fetch_stars(args.username, args.rate_limit)
    formatter = { 'jsonl': to_jsonl, 'json': to_json }
    formatter = formatter[args.format]
    output = formatter(stars)
    for entry in output:
        print(entry)
    sys.exit(0)


if __name__ == "__main__":
    main()
