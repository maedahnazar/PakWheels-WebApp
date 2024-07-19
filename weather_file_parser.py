import csv
import os
from datetime import datetime

from weather_reading import WeatherReading
from weather_records import WeatherRecords


class WeatherFileParser:
    def find_date_field(self, header_row):
        date_field = None
        for field in header_row:
            datetime.strptime(header_row[field], "%Y-%m-%d")
            date_field = field
            break
        return date_field 

    def parse_weather_file(self, reader, date_field):
        weather_records = WeatherRecords()
        for row in reader:
            date = row.get(date_field)
            if not date:
                continue
            stripped_row = {key.strip(): value.strip() for key, value in row.items()}

            weather_reading = WeatherReading(
                date,
                stripped_row.get("Max TemperatureC"),
                stripped_row.get("Min TemperatureC"),
                stripped_row.get("Mean TemperatureC"),
                stripped_row.get("Max Humidity"),
                stripped_row.get("Mean Humidity") or stripped_row.get("  Mean Humidity"),
                stripped_row.get("Min Humidity") or stripped_row.get("  Min Humidity")
            )
            weather_records.add_weather_reading(weather_reading)
        return weather_records

    def parse_files(self, directory):
        weather_records = WeatherRecords()
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            with open(file_path, "r") as file:
                dict_reader = csv.DictReader(file)
                date_field = self.find_date_field(next(dict_reader))
                if not date_field:
                    continue

                weather_records.weather_readings.extend(
                    self.parse_weather_file(dict_reader, date_field).weather_readings
                )

        return weather_records if weather_records.weather_readings else None
