import argparse
import sys
from datetime import datetime 
from weatherman_utils import *


def compute_yearly_statistics(weather_data, year):
    highest_temp = float("-inf")
    lowest_temp = float("inf")
    highest_temp_day = None
    lowest_temp_day = None
    highest_humidity = float("-inf")
    highest_humidity_day = None

    for reading in weather_data.readings:
        if reading.date.year == year:
            if reading.max_temp and reading.max_temp > highest_temp:
                highest_temp = reading.max_temp
                highest_temp_day = reading.date
            if reading.min_temp and reading.min_temp < lowest_temp:
                lowest_temp = reading.min_temp
                lowest_temp_day = reading.date
            if reading.max_humidity and reading.max_humidity > highest_humidity:
                highest_humidity = reading.max_humidity
                highest_humidity_day = reading.date

    return highest_temp, highest_temp_day, lowest_temp, lowest_temp_day, highest_humidity, highest_humidity_day

def generate_yearly_report(weather_data, year):
    highest_temp, highest_temp_day, lowest_temp, lowest_temp_day, highest_humidity, highest_humidity_day = (
            compute_yearly_statistics(weather_data, year)
        )
    print(f"Highest: {highest_temp}C on {highest_temp_day.strftime('%B %d')}")
    print(f"Lowest: {lowest_temp}C on {lowest_temp_day.strftime('%B %d')}")
    print(f"Humidity: {highest_humidity}% on {highest_humidity_day.strftime('%B %d')}")

def compute_monthly_averages(weather_data, year, month):
    filtered_readings = filter_readings_by_month(weather_data.readings, year, month)
    total_max_temp, total_min_temp, total_mean_humidity, count = calculate_totals_and_count(filtered_readings)
    return compute_averages(total_max_temp, total_min_temp, total_mean_humidity, count)

def generate_monthly_average_report(weather_data, year, month):
    avg_max_temp, avg_min_temp, avg_mean_humidity = compute_monthly_averages(weather_data, year, month)
    if avg_max_temp is None:
        print("No weather readings available for this month.")
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
    parser = argparse.ArgumentParser(description="Weather Man")
    parser.add_argument("directory", type=str, help="Directory containing weather files")
    parser.add_argument("-e", "--year", type=int, help="Generate yearly weather report for the given year")
    parser.add_argument("-a", "--average", type=str, help="Generate monthly average weather report for the given year/month (YYYY/MM)")
    parser.add_argument("-c", "--chart", type=str, help="Generate monthly weather chart for the given year/month (YYYY/MM)")
    args = parser.parse_args()

    weather_readings= parse_files(args.directory)

    if args.year:
        generate_yearly_report(weather_readings, args.year)

    if args.average:
        year, month = map(int, args.average.split("/"))
        generate_monthly_average_report(weather_readings, year, month)

    if args.chart:
        year, month = map(int, args.chart.split("/"))
        generate_monthly_chart(weather_readings, year, month)

if __name__ == "__main__":
    main()
