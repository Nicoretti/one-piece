from __future__ import annotations

import argparse
import sys
from enum import IntEnum
from pathlib import Path

from pytest_history.queries import flakes, newly_added, results, runs


class ExitCode(IntEnum):
    Success = 0
    Failure = 1


class History:
    class Flakes:
        def __init__(self, parser):
            self._flakes = parser.add_parser(
                "flakes", description="List all flaky tests"
            )
            self._flakes.set_defaults(func=self.print_flakes)

        @staticmethod
        def print_flakes(db, _args) -> ExitCode:
            # TODO: consider adding range argument
            exit_code = ExitCode.Success
            for f in flakes(db):
                print(f"{f.node_id}")
                exit_code = ExitCode.Failure
            return exit_code

    class List:
        def __init__(self, parser):
            self._parser = parser.add_parser("list", description="List historic data")
            self._parser.set_defaults(func=lambda db, args: self._parser.print_help())
            self._subcommands = self._parser.add_subparsers(description="")

            list_results = self._subcommands.add_parser(
                "results", description="List historic test results"
            )
            list_results.add_argument(
                "id",
                type=int,
                help="Id of the test run whose result shall be reported",
            )
            list_results.set_defaults(func=self.print_results)

            list_runs = self._subcommands.add_parser(
                "runs", description="List historic test runs"
            )
            list_runs.set_defaults(func=self.print_runs)

            list_added = self._subcommands.add_parser(
                "added", description="List test added during the most recent run"
            )
            list_added.set_defaults(func=self.print_newly_added)

        @staticmethod
        def print_results(db, args):
            template = "{id} {node_id} {duration} {outcome}"
            for r in results(db, args.id):
                print(
                    template.format(
                        id=r.id,
                        node_id=r.node_id,
                        duration=r.duration,
                        outcome=r.outcome,
                    )
                )
            return ExitCode.Success

        @staticmethod
        def print_runs(db, _args):
            # TODO: consider adding passed, failed, skipped
            template = "{id} {datetime}"
            for r in runs(db):
                print(template.format(id=r.id, datetime=r.start))
            return ExitCode.Success

        @staticmethod
        def print_newly_added(db, _args):
            template = "{id} {node_id} {duration} {outcome}"
            for n in newly_added(db):
                print(
                    template.format(
                        id=n.id,
                        node_id=n.node_id,
                        duration=n.duration,
                        outcome=n.outcome,
                    )
                )
            return ExitCode.Success

    @staticmethod
    def _path(value):
        path = Path(value)
        if not path.exists():
            raise argparse.ArgumentTypeError(f"Database: {value}, does not exist")
        return path

    def __init__(self):
        self._parser = argparse.ArgumentParser(
            "pytest-history",
            description="Provide insights into historic test executions",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        self._parser.add_argument(
            "--db",
            type=self._path,
            default=".test-results.db",
            help="database used for analysing the data.",
        )
        self._parser.set_defaults(func=lambda db, args: self._parser.print_help())
        self._subcommands = self._parser.add_subparsers(description="")
        self._list = self.List(self._subcommands)
        self._flakes = self.Flakes(self._subcommands)

    def parse_args(self, argv=None):
        return self._parser.parse_args(argv)


def _main(argv=None) -> ExitCode:
    p = History()
    args = p.parse_args()
    return args.func(args.db, args)


def main(argv=None):
    try:
        exit_code = _main(argv)
    except Exception as ex:
        print(f"Error occurred, details: {ex}")
        exit_code = ExitCode.Failure

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
