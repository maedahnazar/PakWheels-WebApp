class WeatherRecords:
    def __init__(self):
        self.readings = []

    def add_weather_reading(self, reading):
        self.readings.append(reading)

    def filter_readings_by_month(self, year, month):
        return [
            reading for reading in self.readings 
            if reading.date.year == year and reading.date.month == month
        ]

    def aggregate_weather_data(self, filtered_weather_readings):
        total_max_temperature = 0
        total_min_temperature = 0
        total_mean_humidity = 0
        reading_count = 0

        for reading in filtered_weather_readings:
            if reading.max_temperature:
                total_max_temperature += reading.max_temperature
            if reading.min_temperature:
                total_min_temperature += reading.min_temperature
            if reading.mean_humidity:
                total_mean_humidity += reading.mean_humidity
            reading_count += 1

        return (
            total_max_temperature, 
            total_min_temperature, 
            total_mean_humidity, 
            reading_count
        )

    def compute_weather_averages(
        self, 
        total_max_temperature, 
        total_min_temperature, 
        total_mean_humidity, 
        reading_count
    ):
        if reading_count == 0:
            return None, None, None

        avg_max_temperature = total_max_temperature // reading_count
        avg_min_temperature = total_min_temperature // reading_count
        avg_mean_humidity = total_mean_humidity // reading_count

        return (
            avg_max_temperature, 
            avg_min_temperature, 
            avg_mean_humidity
        )
