import csv
import os
from datetime import datetime

from weather_reading import WeatherReading
from weather_records import WeatherRecords


class WeatherFileParser:
    def find_date_field(self, file_path):
        date_field = None
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            header_row = next(reader)
            for field in header_row:
                datetime.strptime(header_row[field], "%Y-%m-%d")
                date_field = field
                break
            return date_field 

    def parse_weather_file(self, file_path, date_field):
        weather_records = WeatherRecords()
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                date = row.get(date_field)
                if not date:
                    continue
                reading = WeatherReading(
                    date=date,
                    max_temperature=row["Max TemperatureC"].strip(),
                    min_temperature=row["Min TemperatureC"].strip(),
                    mean_temperature=row["Mean TemperatureC"].strip(),
                    max_humidity=row["Max Humidity"].strip(),
                    mean_humidity=row.get("Mean Humidity", "").strip() or 
                                row.get("  Mean Humidity", "").strip(),
                    min_humidity=row.get("Min Humidity", "").strip() or 
                                row.get("  Min Humidity", "").strip()
                )
                weather_records.add_weather_reading(reading)
        return weather_records

    def parse_files(self, directory):
        weather_records = WeatherRecords()
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            date_field = self.find_date_field(file_path)
            if not date_field:
                continue
            file_weather_records = self.parse_weather_file(file_path, date_field)
            weather_records.readings.extend(file_weather_records.readings)
        return weather_records if weather_records.readings else None
