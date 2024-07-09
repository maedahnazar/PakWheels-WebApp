import argparse
import csv
import os
import sys
from datetime import datetime


def parse_int(value):
    return int(value) if value else None


def validate_weather_file(reader, expected_columns):
    fieldnames = [field.strip() for field in reader.fieldnames]
    return any(col in fieldnames for col in expected_columns)


class WeatherReading:
    def __init__(self, date, max_temp, mean_temp, min_temp, max_humidity, mean_humidity, min_humidity):
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.max_temp = parse_int(max_temp)
        self.mean_temp = parse_int(mean_temp)
        self.min_temp = parse_int(min_temp)
        self.max_humidity = parse_int(max_humidity)
        self.mean_humidity = parse_int(mean_humidity)
        self.min_humidity = parse_int(min_humidity)


class WeatherData:
    def __init__(self):
        self.readings = []

    def add_reading(self, reading):
        self.readings.append(reading)


def parse_files(directory):
    weather_data = WeatherData()
    expected_columns = {"PKT", "PKST"}
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                if not validate_weather_file(reader, expected_columns):
                    print(f"Skipping file {filename}: missing required columns")
                    continue
                for row in reader:
                    date = row.get("PKT") or row.get("PKST")
                    try:
                        if date:
                            reading = WeatherReading(
                                date=date,
                                max_temp=row["Max TemperatureC"],
                                min_temp=row["Min TemperatureC"],
                                mean_temp=row["Mean TemperatureC"],
                                max_humidity=row["Max Humidity"],
                                mean_humidity=row.get("Mean Humidity", "").strip() or row.get("  Mean Humidity", "").strip(),
                                min_humidity=row.get("Min Humidity", "").strip() or row.get("  Min Humidity", "").strip()
                            )
                            weather_data.add_reading(reading)
                    except:
                        print(f"Skipping invalid data in {filename}{row}")
    return weather_data

def compute_yearly_statistics(weather_data, year):
    highest_temp = float('-inf')
    lowest_temp = float('inf')
    highest_temp_day = None
    lowest_temp_day = None
    highest_humidity = float('-inf')
    highest_humidity_day = None

    for reading in weather_data.readings:
        if reading.date.year == year:
            if reading.max_temp is not None and reading.max_temp > highest_temp:
                highest_temp = reading.max_temp
                highest_temp_day = reading.date
            if reading.min_temp is not None and reading.min_temp < lowest_temp:
                lowest_temp = reading.min_temp
                lowest_temp_day = reading.date
            if reading.max_humidity is not None and reading.max_humidity > highest_humidity:
                highest_humidity = reading.max_humidity
                highest_humidity_day = reading.date

    return highest_temp, highest_temp_day, lowest_temp, lowest_temp_day, highest_humidity, highest_humidity_day


def generate_yearly_report(weather_data, year):
    highest_temp, highest_temp_day, lowest_temp, lowest_temp_day, highest_humidity, highest_humidity_day = compute_yearly_statistics(weather_data, year)
    print(f"Highest: {highest_temp}C on {highest_temp_day.strftime('%B %d')}")
    print(f"Lowest: {lowest_temp}C on {lowest_temp_day.strftime('%B %d')}")
    print(f"Humidity: {highest_humidity}% on {highest_humidity_day.strftime('%B %d')}")


def compute_monthly_averages(weather_data, year, month):
    total_max_temp = 0
    total_min_temp = 0
    total_mean_humidity = 0
    count = 0

    for reading in weather_data.readings:
        if reading.date.year == year and reading.date.month == month:
            if reading.max_temp is not None:
                total_max_temp += reading.max_temp
            if reading.min_temp is not None:
                total_min_temp += reading.min_temp
            if reading.mean_humidity is not None:
                total_mean_humidity += reading.mean_humidity
            count += 1

    if count == 0:
        return None, None, None

    return total_max_temp // count, total_min_temp // count, total_mean_humidity // count


def generate_monthly_average_report(weather_data, year, month):
    avg_max_temp, avg_min_temp, avg_mean_humidity = compute_monthly_averages(weather_data, year, month)
    if avg_max_temp is None:
        print("No data available for this month.")
    else:
        print(f"Highest Average: {avg_max_temp}C")
        print(f"Lowest Average: {avg_min_temp}C")
        print(f"Average Mean Humidity: {avg_mean_humidity}%")


def generate_monthly_chart(weather_data, year, month):
    print(f"{datetime(year, month, 1).strftime('%B %Y')}")
    for reading in weather_data.readings:
        if reading.date.year == year and reading.date.month == month:
            if reading.max_temp is not None and reading.min_temp is not None:
                print(f"{reading.date.day:02d} {'+' * reading.max_temp} {reading.max_temp}C")
                print(f"{reading.date.day:02d} {'+' * reading.min_temp} {reading.min_temp}C")


def main():
    parser = argparse.ArgumentParser(description='Weather Man')
    parser.add_argument('directory', type=str, help='Directory containing weather files')
    parser.add_argument('-e', '--year', type=int, help='Generate yearly report for given year')
    parser.add_argument('-a', '--average', type=str, help='Generate monthly average report for given year/month (YYYY/MM)')
    parser.add_argument('-c', '--chart', type=str, help='Generate monthly chart for given year/month (YYYY/MM)')
    args = parser.parse_args()

    weather_data = parse_files(args.directory)

    if args.year:
        generate_yearly_report(weather_data, args.year)

    if args.average:
        year, month = map(int, args.average.split('/'))
        generate_monthly_average_report(weather_data, year, month)

    if args.chart:
        year, month = map(int, args.chart.split('/'))
        generate_monthly_chart(weather_data, year, month)


if __name__ == '__main__':
    main()
