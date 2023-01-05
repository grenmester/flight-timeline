"""Extract flight information into JSON."""

import glob
import json
import os

import click

OUTPUT_DIR = "src/data"
OUTPUT_FILE = "flights.json"


def get_source_files(root_dir):
    """
    Find all org files under the given directory and return them in
    chronological order.
    """
    return sorted(glob.iglob(f"{root_dir}/**/*.org", recursive=True))


def get_flight(date, start_airport, start_time, end_airport, end_time):
    """
    Parse the flight information from a single flight.
    """
    return {
        "start_date": date,
        "start_airport": start_airport,
        "start_time": start_time,
        "end_airport": end_airport,
        "end_time": end_time,
    }


def get_flights(file_name):
    """
    Extract and return all flight information from a source file.
    """
    with open(file_name, "r", encoding="utf8") as file:
        date, flights = "", []
        for line in file.readlines():
            match line.split():
                # Date info
                case ["*", month, day, year]:
                    date = f"{month} {day} {year}"
                # Flight info
                case [
                    "-",
                    "flight",
                    airports,
                    start_time,
                    start_suffix,
                    "-",
                    end_time,
                    end_suffix,
                ]:
                    start_airport, end_airport = airports.split("-")
                    flights.append(
                        get_flight(
                            date,
                            start_airport,
                            f"{start_time} {start_suffix}",
                            end_airport,
                            f"{end_time} {end_suffix}",
                        )
                    )

    return flights


@click.command()
@click.option(
    "-r",
    "--root-dir",
    type=click.Path(),
    help="Path to input root directory.",
)
def main(root_dir):
    """
    Given an input root directory, extract all flight information from all
    source files and output to a JSON file.
    """
    data = []
    for file_name in get_source_files(root_dir):
        data.extend(get_flights(file_name))

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(f"{OUTPUT_DIR}/{OUTPUT_FILE}", "w", encoding="utf8") as file:
        json.dump(data, file)


if __name__ == "__main__":
    main()  # pylint: disable = no-value-for-parameter
