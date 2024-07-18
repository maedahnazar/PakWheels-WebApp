from datetime import datetime


class WeatherReportPrinter:
    def print_yearly_report(
        highest_temperature, 
        highest_temperature_day, 
        lowest_temperature, 
        lowest_temperature_day, 
        highest_humidity, 
        highest_humidity_day
    ):
        print(f"Highest: {highest_temperature}C on {highest_temperature_day.strftime('%B %d')}")
        print(f"Lowest: {lowest_temperature}C on {lowest_temperature_day.strftime('%B %d')}")
        print(f"Humidity: {highest_humidity}% on {highest_humidity_day.strftime('%B %d')}")

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
            if (reading.date.year != year or reading.date.month != month or 
            not (reading.max_temperature and reading.min_temperature)):
                continue
            print(f"{reading.date.day:02d} {'+' * reading.max_temperature} {reading.max_temperature}C")
            print(f"{reading.date.day:02d} {'+' * reading.min_temperature} {reading.min_temperature}C")
