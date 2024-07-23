import csv
import os
import re
import calendar
from datetime import datetime

from weather_reading import WeatherReading
from weather_records import WeatherRecords


class WeatherFileParser:
    selected_weather_attributes = {}

    def extract_header_indices(self, weather_file_reader):
        header_fields = [field.strip() for field in next(weather_file_reader)]

        required_weather_attributes = [
            ("PKT", "PKST"), "Max TemperatureC", "Min TemperatureC", "Max Humidity", "Mean Humidity"
        ]

        for attribute_group in required_weather_attributes:
            if isinstance(attribute_group, tuple):
                matching_weather_attribute = next((attr for attr in attribute_group if attr in header_fields), None)
                if matching_weather_attribute:
                    self.selected_weather_attributes[attribute_group] = matching_weather_attribute
            else:
                if attribute_group in header_fields:
                    self.selected_weather_attributes[attribute_group] = attribute_group

        if not all(attr in self.selected_weather_attributes for attr in required_weather_attributes):
            raise ValueError("Missing required weather attributes in the header.")


    def parse_weather_file(self, weather_file_path):
        weather_records = WeatherRecords()

        with open(weather_file_path, "r") as file:
            weather_file_reader = csv.DictReader(file)
            self.extract_header_indices(weather_file_reader)
            
            for weather_data_row in weather_file_reader:
                observation_date = weather_data_row.get(self.selected_weather_attributes.get(("PKT", "PKST")))
                if not observation_date:
                    continue
                
                cleaned_row = {key.strip(): value.strip() for key, value in weather_data_row.items()}
                
                weather_reading = WeatherReading(
                    observation_date,
                    cleaned_row.get("Max TemperatureC"),
                    cleaned_row.get("Min TemperatureC"),
                    cleaned_row.get("Mean TemperatureC"),
                    cleaned_row.get("Max Humidity"),
                    cleaned_row.get("Mean Humidity") or cleaned_row.get("  Mean Humidity"),
                    cleaned_row.get("Min Humidity") or cleaned_row.get("  Min Humidity")
                )
                weather_records.add_weather_reading(weather_reading)
        
        return weather_records

    def parse_weather_files_in_directory(self, weather_files_directory_path):
        weather_records = WeatherRecords()
        valid_months = list(calendar.month_abbr[1:])  
        
        for weather_file_name in os.listdir(weather_files_directory_path):
            match = re.match(r"Murree_weather_(\d{4})_(\w+).txt", weather_file_name)
            year_str, month_str = match.groups()
            
            if not (year_str.isdigit() and month_str.capitalize() in valid_months) or not match:
                continue  
            
            weather_file_path = os.path.join(weather_files_directory_path, weather_file_name)
            
            file_weather_records = self.parse_weather_file(weather_file_path)
            if file_weather_records.weather_readings:
                weather_records.weather_readings.extend(file_weather_records.weather_readings)
        
        return weather_records if weather_records.weather_readings else None
    