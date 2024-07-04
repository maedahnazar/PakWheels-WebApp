import os
import csv
import sys
from datetime import datetime

class WeatherReading:
    def __init__(self, date, max_temp, mean_temp, min_temp, dew_point, mean_dew_point, min_dew_point, max_humidity, mean_humidity, min_humidity, max_pressure, mean_pressure, min_pressure, max_visibility, mean_visibility, min_visibility, max_wind_speed, mean_wind_speed, max_gust_speed, precipitation, cloud_cover, events, wind_dir_degrees):
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.max_temp = self.parse_int(max_temp)
        self.mean_temp = self.parse_int(mean_temp)
        self.min_temp = self.parse_int(min_temp)
        self.dew_point = self.parse_int(dew_point)
        self.mean_dew_point = self.parse_int(mean_dew_point)
        self.min_dew_point = self.parse_int(min_dew_point)
        self.max_humidity = self.parse_int(max_humidity)
        self.mean_humidity = self.parse_int(mean_humidity)
        self.min_humidity = self.parse_int(min_humidity)
        self.max_pressure = self.parse_float(max_pressure)
        self.mean_pressure = self.parse_float(mean_pressure)
        self.min_pressure = self.parse_float(min_pressure)
        self.max_visibility = self.parse_float(max_visibility)
        self.mean_visibility = self.parse_float(mean_visibility)
        self.min_visibility = self.parse_float(min_visibility)
        self.max_wind_speed = self.parse_int(max_wind_speed)
        self.mean_wind_speed = self.parse_int(mean_wind_speed)
        self.max_gust_speed = self.parse_int(max_gust_speed)
        self.precipitation = self.parse_float(precipitation)
        self.cloud_cover = self.parse_int(cloud_cover)
        self.events = events
        self.wind_dir_degrees = self.parse_int(wind_dir_degrees)
    
    def parse_int(self, value):
        return int(value) if value else None

    def parse_float(self, value):
        return float(value) if value else None

class WeatherData:
    def __init__(self):
        self.readings = []

    def add_reading(self, reading):
        self.readings.append(reading)

def parse_files(directory):
    weather_data = WeatherData()
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename)) as file:
                reader = csv.reader(file)
                next(reader)  # skip header
                for row in reader:
                    if row[0]:
                        reading = WeatherReading(*row[:23])  # there are 23 columns to be read
                        weather_data.add_reading(reading)
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
    for reading in weather_data.readings:
        if reading.date.year == year and reading.date.month == month:
            if reading.max_temp is not None and reading.min_temp is not None:
                print(f"{reading.date.day:02d} {'+' * reading.max_temp}{'+' * reading.min_temp} {reading.min_temp}C - {reading.max_temp}C")

                

# def generate_combined_monthly_chart(weather_data, year, month):
#     print(f"{datetime(year, month, 1).strftime('%B %Y')}")
#     for reading in weather_data.readings:
#         if reading.date.year == year and reading.date.month == month:
#             if reading.max_temp is not None and reading.min_temp is not None:
#                 print(f"{reading.date.day:02d} {'+' * reading.max_temp} {'+' * reading.min_temp} {reading.min_temp} - {reading.max_temp}C")

def main():
    import argparse
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
