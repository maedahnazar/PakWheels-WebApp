from datetime import datetime


class WeatherReading:
    def __init__(
        self, 
        date, 
        max_temperature, 
        mean_temperature, 
        min_temperature, 
        max_humidity, 
        mean_humidity, 
        min_humidity
    ):
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.max_temperature = self.parse_int(max_temperature)
        self.mean_temperature = self.parse_int(mean_temperature)
        self.min_temperature = self.parse_int(min_temperature)
        self.max_humidity = self.parse_int(max_humidity)
        self.mean_humidity = self.parse_int(mean_humidity)
        self.min_humidity = self.parse_int(min_humidity)

    def parse_int(self, value):
        return int(value) if value else None

    def parse_float(self, value):
        return float(value) if value else None
