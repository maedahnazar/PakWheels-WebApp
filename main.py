import argparse

from weather_file_parser import WeatherFileParser
from weather_statistics import WeatherStatistics


def main():
    parser = argparse.ArgumentParser(description="Weather Man")
    parser.add_argument(
        "directory", 
        type=str, 
        help="Directory containing weather files"
    )
    parser.add_argument(
        "-e", 
        "--year", 
        type=int, 
        help="Generate yearly weather report for the given year"
    )
    parser.add_argument(
        "-a", 
        "--average", 
        type=str, 
        help="Generate monthly average weather report for the given year/month (YYYY/MM)"
    )
    parser.add_argument(
        "-c", 
        "--chart", 
        type=str, 
        help="Generate monthly weather chart for the given year/month (YYYY/MM)"
    )

    args = parser.parse_args()
    weather_parser = WeatherFileParser()
    weather_readings = weather_parser.parse_files(args.directory)

    if not weather_readings:
        return

    weather_stats = WeatherStatistics(weather_readings)

    if args.year:
        weather_stats.generate_yearly_report(args.year)

    if args.average:
        year, month = map(int, args.average.split("/"))
        weather_stats.generate_monthly_average_report(year, month)

    if args.chart:
        year, month = map(int, args.chart.split("/"))
        weather_stats.generate_monthly_chart(year, month)


if __name__ == "__main__":
    main()
