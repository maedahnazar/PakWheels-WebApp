import csv
import os
from datetime import datetime


def parse_int(value):
    return int(value) if value else None

def parse_float(value):
    return float(value) if value else None

def get_date(row):
    if "PKT" in row:
        return row["PKT"]
    elif "PKST" in row:
        return row["PKST"]
    return None

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

def filter_readings_by_month(readings, year, month):
    return [reading for reading in readings if reading.date.year == year and 
            reading.date.month == month]

def calculate_totals_and_count(filtered_readings):
    total_max_temp = 0
    total_min_temp = 0
    total_mean_humidity = 0
    count = 0

    for reading in filtered_readings:
        if reading.max_temp is not None:
            total_max_temp += reading.max_temp
        if reading.min_temp is not None:
            total_min_temp += reading.min_temp
        if reading.mean_humidity is not None:
            total_mean_humidity += reading.mean_humidity
        count += 1

    return total_max_temp, total_min_temp, total_mean_humidity, count

def compute_averages(total_max_temp, total_min_temp, total_mean_humidity, count):
    if count == 0:
        return None, None, None

    avg_max_temp = total_max_temp // count
    avg_min_temp = total_min_temp // count
    avg_mean_humidity = total_mean_humidity // count

    return avg_max_temp, avg_min_temp, avg_mean_humidity


def parse_files(directory):
    weather_data = WeatherData()
    expected_columns = {"PKT", "PKST"}
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if is_weather_file(file_path, expected_columns):
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    date = get_date(row)
                    if date:
                        reading = WeatherReading(
                            date=date,
                            max_temp=row["Max TemperatureC"].strip(),
                            min_temp=row["Min TemperatureC"].strip(),
                            mean_temp=row["Mean TemperatureC"].strip(),
                            max_humidity=row["Max Humidity"].strip(),
                            mean_humidity=row.get("Mean Humidity", "").strip() or row.get("  Mean Humidity", "").strip(),
                            min_humidity=row.get("Min Humidity", "").strip() or row.get("  Min Humidity", "").strip()
                        )
                        weather_data.add_reading(reading)
    return weather_data if weather_data.readings else None

def is_weather_file(file_path, expected_columns):
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            fieldnames = {field.strip() for field in reader.fieldnames}

            if not expected_columns.intersection(fieldnames):
                print(f"Skipping file {file_path}: Missing required columns")
                return False
            return True
    except Exception as e:
        print(f"Error checking file {file_path}: {e}")
        return False

