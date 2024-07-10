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
    def __init__(self, date, max_temperature, mean_temperature, min_temperature, max_humidity, mean_humidity, min_humidity):
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.max_temperature = parse_int(max_temperature)
        self.mean_temperature = parse_int(mean_temperature)
        self.min_temperature = parse_int(min_temperature)
        self.max_humidity = parse_int(max_humidity)
        self.mean_humidity = parse_int(mean_humidity)
        self.min_humidity = parse_int(min_humidity)

class WeatherData:
    def __init__(self):
        self.readings = []

    def add_reading(self, reading):
        self.readings.append(reading)


def filter_readings_by_month(readings, year, month):
    return [
        reading for reading in readings if reading.date.year == year and reading.date.month == month
    ]   

def calculate_totals_and_count(filtered_readings):
    total_max_temperature = 0
    total_min_temperature = 0
    total_mean_humidity = 0
    count = 0

    for reading in filtered_readings:
        if reading.max_temperature is not None:
            total_max_temperature += reading.max_temperature
        if reading.min_temperature is not None:
            total_min_temperature += reading.min_temperature
        if reading.mean_humidity is not None:
            total_mean_humidity += reading.mean_humidity
        count += 1

    return total_max_temperature, total_min_temperature, total_mean_humidity, count

def compute_averages(total_max_temperature, total_min_temperature, total_mean_humidity, count):
    if count == 0:
        avg_max_temperature, avg_min_temperature, avg_mean_humidity = None, None, None

    avg_max_temperature = total_max_temperature // count
    avg_min_temperature = total_min_temperature // count
    avg_mean_humidity = total_mean_humidity // count

    return avg_max_temperature, avg_min_temperature, avg_mean_humidity


def parse_weather_file(file_path):
    weather_data = WeatherData()
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = get_date(row)
            if date:
                reading = WeatherReading(
                    date=date,
                    max_temperature=row["Max TemperatureC"].strip(),
                    min_temperature=row["Min TemperatureC"].strip(),
                    mean_temperature=row["Mean TemperatureC"].strip(),
                    max_humidity=row["Max Humidity"].strip(),
                    mean_humidity=row.get("Mean Humidity", "").strip() or row.get("  Mean Humidity", "").strip(),
                    min_humidity=row.get("Min Humidity", "").strip() or row.get("  Min Humidity", "").strip()
                )
                weather_data.add_reading(reading)
    return weather_data

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

def parse_files(directory):
    weather_data = WeatherData()
    expected_columns = {"PKT", "PKST"}
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if is_weather_file(file_path, expected_columns):
            file_weather_data = parse_weather_file(file_path)
            weather_data.readings.extend(file_weather_data.readings)
    return weather_data if weather_data.readings else None