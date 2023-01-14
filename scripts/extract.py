"""Extract flight information into JSON."""

import datetime as dt
import glob
import json
import os

import click

TZ_FILE = "scripts/data/tz.json"
OUTPUT_DIR = "src/data"
OUTPUT_FILE = "flights.json"


def get_source_files(root_dir):
    """
    Find all org files under the given directory and return them in
    chronological order.
    """
    return sorted(glob.iglob(f"{root_dir}/**/*.org", recursive=True))


def format_tz(tz):
    """
    Format the time zone string.
    """
    if tz[4] == "0":
        tz = tz[:4] + tz[5:]
    return tz[:-2]


def get_flight(date, start_airport, start_time, end_airport, end_time):
    """
    Parse the flight information from a single flight.
    """
    with open(TZ_FILE, "r", encoding="utf8") as file:
        tz_dict = json.load(file)

    start_dt = dt.datetime.strptime(
        f"{date} {start_time} {tz_dict[start_airport]}", "%b %d, %Y %I:%M %p %Z%z"
    )
    end_dt = dt.datetime.strptime(
        f"{date} {end_time} {tz_dict[end_airport]}", "%b %d, %Y %I:%M %p %Z%z"
    )
    next_day = False
    if end_dt < start_dt:
        end_dt += dt.timedelta(days=1)
        next_day = True
    total_minutes = (end_dt - start_dt).seconds // 60
    hours = total_minutes // 60
    minutes = total_minutes % 60

    return {
        "start_date": date,
        "start_airport": start_airport,
        "start_time": start_time,
        "start_tz": format_tz(tz_dict[start_airport]),
        "end_airport": end_airport,
        "end_time": end_time,
        "end_tz": format_tz(tz_dict[end_airport]),
        "flight_duration": f"{hours}h {minutes}m",
        "next_day": next_day,
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
