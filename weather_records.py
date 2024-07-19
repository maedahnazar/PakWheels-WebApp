class WeatherRecords:
    def __init__(self):
        self.weather_readings = []

    def add_weather_reading(self, weather_reading):
        self.weather_readings.append(weather_reading)

    def filter_weather_readings_by_month(self, year, month):
        return [
            weather_reading for weather_reading in self.weather_readings 
            if weather_reading.date.year == year and 
            weather_reading.date.month == month and
            weather_reading.max_temperature and 
            weather_reading.min_temperature
        ]
    
    def aggregate_weather_data(self, filtered_weather_readings):
        total_max_temperature = 0
        total_min_temperature = 0
        total_mean_humidity = 0
        weather_reading_count = 0

        for weather_reading in filtered_weather_readings:
            if weather_reading.max_temperature:
                total_max_temperature += weather_reading.max_temperature
            if weather_reading.min_temperature:
                total_min_temperature += weather_reading.min_temperature
            if weather_reading.mean_humidity:
                total_mean_humidity += weather_reading.mean_humidity
            weather_reading_count += 1

        return (
            total_max_temperature, 
            total_min_temperature, 
            total_mean_humidity, 
            weather_reading_count
        )

    def compute_weather_averages(
        self, 
        total_max_temperature, 
        total_min_temperature, 
        total_mean_humidity, 
        weather_reading_count
    ):
        if weather_reading_count == 0:
            return None, None, None

        avg_max_temperature = total_max_temperature // weather_reading_count
        avg_min_temperature = total_min_temperature // weather_reading_count
        avg_mean_humidity = total_mean_humidity // weather_reading_count

        return (
            avg_max_temperature, 
            avg_min_temperature, 
            avg_mean_humidity
        )
