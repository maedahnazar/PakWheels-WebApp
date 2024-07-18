from weather_report_printer import WeatherReportPrinter


class WeatherStatistics:
    def __init__(self, weather_readings):
        self.weather_readings = weather_readings

    def compute_yearly_statistics(self, year):
        highest_temperature = float("-inf")
        lowest_temperature = float("inf")
        highest_temperature_day = None
        lowest_temperature_day = None
        highest_humidity = float("-inf")
        highest_humidity_day = None

        for reading in self.weather_readings.readings:
            if reading.date.year != year:
                continue

            if reading.max_temperature and reading.max_temperature > highest_temperature:
                highest_temperature = reading.max_temperature
                highest_temperature_day = reading.date
            if reading.min_temperature and reading.min_temperature < lowest_temperature:
                lowest_temperature = reading.min_temperature
                lowest_temperature_day = reading.date
            if reading.max_humidity and reading.max_humidity > highest_humidity:
                highest_humidity = reading.max_humidity
                highest_humidity_day = reading.date

        return (
            highest_temperature, 
            highest_temperature_day,
            lowest_temperature, 
            lowest_temperature_day, 
            highest_humidity, 
            highest_humidity_day
        )

    def generate_yearly_report(self, year):
        WeatherReportPrinter.print_yearly_report (
            *self.compute_yearly_statistics(year)
        )

    def compute_monthly_averages(self, year, month):
        filtered_readings = self.weather_readings.filter_readings_by_month(year, month)
        total_max_temperature, total_min_temperature, total_mean_humidity, count = (
            self.weather_readings.aggregate_weather_data(filtered_readings)
        )
        return self.weather_readings.compute_weather_averages (
            total_max_temperature, 
            total_min_temperature, 
            total_mean_humidity, 
            count
        )

    def generate_monthly_average_report(self, year, month):
        WeatherReportPrinter.print_monthly_average_report (
            *self.compute_monthly_averages(year, month)
        )

    def generate_monthly_chart(self, year, month):
        WeatherReportPrinter.print_monthly_chart(self.weather_readings, year, month)
