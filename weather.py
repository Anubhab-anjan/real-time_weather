import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name:")
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temp_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setFixedSize(600, 400)
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        # Center align
        for widget in [self.city_label, self.city_input, self.temp_label,
                       self.emoji_label, self.description_label]:
            widget.setAlignment(Qt.AlignCenter)

        # Styling
        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family:calibri;
            }
            QLabel#city_label{
                font-size: 30px;
                font-weight: bold;
            }
            QLineEdit#city_input{
                font-size: 20px;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
            QPushButton#get_weather_button{
                font-size: 20px;
                padding: 10px;
                font-weight: bold;
                border-radius: 5px;
                background-color: hsl(200, 100%, 85%);
            }
            QPushButton#get_weather_button:hover{
                background-color: hsl(200, 100%, 75%);
            }
            QLabel#temp_label{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#emoji_label{
                font-size: 50px;
                font-family: Segoe UI Emoji;
            }
            QLabel#description_label{
                font-size: 30px;
                font-style: italic;
            }
        """)

        # IDs for stylesheet
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temp_label.setObjectName("temp_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # Connect button
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "70f03406b3a3f037defe4d0f2f92a0e2"
        city = self.city_input.text().strip()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.display_weather(data)
        except requests.exceptions.HTTPError:
            self.display_error("City not found")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error")
        except requests.exceptions.Timeout:
            self.display_error("Request Timeout")
        except requests.exceptions.RequestException as req_err:
            self.display_error(f"Request Error: {req_err}")

    def display_error(self, message):
        self.temp_label.setText(message)
        self.emoji_label.setText("")
        self.description_label.setText("")

    def display_weather(self, data):
        # Convert temperature
        temperature = data["main"]["temp"] - 273.15
        temperature_celsius = round(temperature, 2)
        self.temp_label.setText(f"Temperature: {temperature_celsius}°C")

        # Weather description
        weather_description = data["weather"][0]["description"]
        self.description_label.setText(f"Description: {weather_description.capitalize()}")

        # Emoji
        weather_id = data["weather"][0]["id"]
        emoji = self.get_weather_emoji(weather_id)
        self.emoji_label.setText(emoji)

    @staticmethod
    def get_weather_emoji(weather_id: int) -> str:
        if 200 <= weather_id < 300:
            return "⛈️"  # Thunderstorm
        elif 300 <= weather_id < 400:
            return "🌦️"  # Drizzle
        elif 500 <= weather_id < 600:
            return "🌧️"  # Rain
        elif 600 <= weather_id < 700:
            return "❄️"  # Snow
        elif 700 <= weather_id < 800:
            return "🌫️"  # Atmosphere
        elif weather_id == 800:
            return "☀️"  # Clear
        elif 801 <= weather_id < 900:
            return "🌥️"  # Clouds
        else:
            return "❓"  # Unknown


if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
