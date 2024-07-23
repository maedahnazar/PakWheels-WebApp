class WeatherRecords:
    def __init__(self):
        self.weather_readings = []  
        self.total_weather_values = {}  
        self.weather_reading_count = 0  
        self.max_weather_records = {}  
        self.min_weather_records = {}  

    def add_weather_reading(self, weather_reading):
        self.weather_readings.append(weather_reading)
        self.update_weather_calculations(weather_reading)

    def filter_weather_readings_by_month(self, year, month):
        return [
            reading for reading in self.weather_readings
            if reading.date.year == year and reading.date.month == month
        ]

    def update_weather_calculations(self, weather_reading):
        weather_attributes = {
            'max_temperature': weather_reading.max_temperature,
            'min_temperature': weather_reading.min_temperature,
            'mean_humidity': weather_reading.mean_humidity
        }

        for attribute, value in weather_attributes.items():
            if value:
                if attribute not in self.total_weather_values:
                    self.total_weather_values[attribute] = 0
                    self.max_weather_records[attribute] = weather_reading
                    self.min_weather_records[attribute] = weather_reading
                
                self.total_weather_values[attribute] += value
                if value > getattr(self.max_weather_records[attribute], attribute):
                    self.max_weather_records[attribute] = weather_reading
                if value < getattr(self.min_weather_records[attribute], attribute):
                    self.min_weather_records[attribute] = weather_reading
        
        self.weather_reading_count += 1

    def compute_weather_averages(self):
        if self.weather_reading_count == 0:
            return {attribute: None for attribute in self.total_weather_values}

        return {
            attribute: self.total_weather_values[attribute] / self.weather_reading_count
            for attribute in self.total_weather_values
        }
