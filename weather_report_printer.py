from datetime import datetime


class WeatherReportPrinter:
    def print_yearly_report(
        highest_temperature, 
        highest_temperature_day, 
        lowest_temperature, 
        lowest_temperature_day, 
        highest_humidity, 
        highest_humidity_day
    ):
        print(f"Highest: {highest_temperature}C on {highest_temperature_day.strftime('%B %d')}")
        print(f"Lowest: {lowest_temperature}C on {lowest_temperature_day.strftime('%B %d')}")
        print(f"Humidity: {highest_humidity}% on {highest_humidity_day.strftime('%B %d')}")

    def print_monthly_average_report(self, weather_averages):
        for weather_attribute, average_weather_value in weather_averages.items():
            if average_weather_value:
                if weather_attribute in ['max_temperature', 'min_temperature']:
                    average_str = f"{int(round(average_weather_value))}C"
                elif weather_attribute == 'mean_humidity':
                    average_str = f"{int(round(average_weather_value))}%"
            
            print(f"{weather_attribute.replace('_', ' ').title()}: {average_str}")

    def print_monthly_chart(weather_records, year, month, combined_bar_charts=True):
        filtered_weather_readings = weather_records.filter_weather_readings_by_month(year, month)
        
        for weather_reading in filtered_weather_readings:
            day = weather_reading.date.day
            
            max_temp = int(round(weather_reading.max_temperature)) if weather_reading.max_temperature else 0
            min_temp = int(round(weather_reading.min_temperature)) if weather_reading.min_temperature else 0
            
            high_temperature_bar = '+' * max_temp
            low_temperature_bar = '+' * min_temp
            
            if combined_bar_charts:
                print(f"{day:02d} {low_temperature_bar} {high_temperature_bar} {min_temp}C - {max_temp}C")
            else:
                print(f"{day:02d} {high_temperature_bar} {max_temp}C")
                print(f"{day:02d} {low_temperature_bar} {min_temp}C")
                