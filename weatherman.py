import argparse
import os
from datetime import datetime 

from weatherman_utils import *


class WeatherReportPrinter:    
    def print_yearly_report(
        highest_temperature, 
        highest_temperature_day, 
        lowest_temperature, 
        lowest_temperature_day, 
        highest_humidity, 
        highest_humidity_day
    ):
        print(
            f"Highest: {highest_temperature}C on "
            f"{highest_temperature_day.strftime('%B %d')}"
        )
        print(
            f"Lowest: {lowest_temperature}C on "
            f"{lowest_temperature_day.strftime('%B %d')}"
        )
        print(
            f"Humidity: {highest_humidity}% on "
            f"{highest_humidity_day.strftime('%B %d')}"
        )

    def print_monthly_average_report(
        avg_max_temperature, 
        avg_min_temperature, 
        avg_mean_humidity
    ):
            print(f"Highest Average: {avg_max_temperature}C")
            print(f"Lowest Average: {avg_min_temperature}C")
            print(f"Average Mean Humidity: {avg_mean_humidity}%")

    def print_monthly_chart(weather_readings, year, month):
        print(f"{datetime(year, month, 1).strftime('%B %Y')}")
        for reading in weather_readings.readings:
            if reading.date.year != year or reading.date.month != month:
                continue
            if not(reading.max_temperature and reading.min_temperature):
                continue
            print(
                f"{reading.date.day:02d} {'+' * reading.max_temperature}"
                f" {reading.max_temperature}C"
            )
            print(
                f"{reading.date.day:02d} {'+' * reading.min_temperature}"
                f" {reading.min_temperature}C"
            )

def compute_yearly_statistics(weather_readings, year):
    highest_temperature = float("-inf")
    lowest_temperature = float("inf")
    highest_temperature_day = None
    lowest_temperature_day = None
    highest_humidity = float("-inf")
    highest_humidity_day = None

    for reading in weather_readings.readings:
        if reading.date.year == year:
            if reading.max_temperature and reading.max_temperature > highest_temperature:
                highest_temperature = reading.max_temperature
                highest_temperature_day = reading.date
            if reading.min_temperature and reading.min_temperature < lowest_temperature:
                lowest_temperature = reading.min_temperature
                lowest_temperature_day = reading.date
            if reading.max_humidity and reading.max_humidity > highest_humidity:
                highest_humidity = reading.max_humidity
                highest_humidity_day = reading.date

    return (
        highest_temperature, 
        highest_temperature_day,
        lowest_temperature, 
        lowest_temperature_day, 
        highest_humidity, 
        highest_humidity_day
    )

def generate_yearly_report(weather_readings, year):
    stats = compute_yearly_statistics(weather_readings, year)
    WeatherReportPrinter.print_yearly_report(*stats)

def compute_monthly_averages(weather_readings, year, month):
    filtered_readings = filter_readings_by_month(
        weather_readings.readings, year, month)
    total_max_temperature, total_min_temperature, total_mean_humidity, count = (
        aggregate_weather_data(filtered_readings)
    )
    return compute_averages(
        total_max_temperature, 
        total_min_temperature, 
        total_mean_humidity, count
    )

def generate_monthly_average_report(weather_readings, year, month):
    averages = compute_monthly_averages(weather_readings, year, month)
    WeatherReportPrinter.print_monthly_average_report(*averages)

def generate_monthly_chart(weather_readings, year, month):
    WeatherReportPrinter.print_monthly_chart(weather_readings, year, month)

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
    weather_readings = parse_files(args.directory)

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
