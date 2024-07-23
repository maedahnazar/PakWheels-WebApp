from weather_report_printer import WeatherReportPrinter
from weather_records import WeatherRecords


class WeatherStatistics:
    def __init__(self, weather_records):
        self.weather_records = weather_records
    
    def compute_yearly_statistics(self, year):
        highest_temperature = float("-inf")
        lowest_temperature = float("inf")
        highest_temperature_day = None
        lowest_temperature_day = None
        highest_humidity = float("-inf")
        highest_humidity_day = None

        for weather_reading in self.weather_records.weather_readings:
            if weather_reading.date.year != year:
                continue

            if weather_reading.max_temperature and weather_reading.max_temperature > highest_temperature:
                highest_temperature = weather_reading.max_temperature
                highest_temperature_day = weather_reading.date
            if weather_reading.min_temperature and weather_reading.min_temperature < lowest_temperature:
                lowest_temperature = weather_reading.min_temperature
                lowest_temperature_day = weather_reading.date
            if weather_reading.max_humidity and weather_reading.max_humidity > highest_humidity:
                highest_humidity = weather_reading.max_humidity
                highest_humidity_day = weather_reading.date

        return (
            highest_temperature, 
            highest_temperature_day,
            lowest_temperature, 
            lowest_temperature_day, 
            highest_humidity, 
            highest_humidity_day
        )

    def generate_yearly_report(self, year):
        WeatherReportPrinter.print_yearly_report(
            *self.compute_yearly_statistics(year)
        )

    def compute_monthly_averages(self, year, month):
        filtered_weather_readings = self.weather_records.filter_weather_readings_by_month(year, month)

        if filtered_weather_readings:
            self.weather_records.update_weather_calculations(filtered_weather_readings)
            weather_averages = self.weather_records.compute_weather_averages()
            return weather_averages

    def generate_monthly_average_report(self, year, month):
        filtered_weather_readings = self.weather_records.filter_weather_readings_by_month(year, month)
        
        for weather_reading in filtered_weather_readings:
            self.weather_records.update_weather_calculations(weather_reading)
        
        weather_averages = self.weather_records.compute_weather_averages()
        WeatherReportPrinter().print_monthly_average_report(weather_averages)

    def generate_monthly_chart(self, year, month):
        WeatherReportPrinter.print_monthly_chart(
            self.weather_records, year, month
        )
        