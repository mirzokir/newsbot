import telebot
import requests
from datetime import datetime, timedelta

TOKEN = '6762831128:AAF-2aCsxx2APxfguirpxugi6LDZKr1QNAg'
bot = telebot.TeleBot(TOKEN)


def get_three_day_forecast(city_name, api_key):
    current_date = datetime.now().date()
    next_three_days = [current_date + timedelta(days=i) for i in range(1, 4)]

    forecast_data = []

    for date in next_three_days:
        date_str = date.strftime('%Y-%m-%d')
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric"
        response = requests.get(url)
        forecast = response.json()
        forecast_data.append((date_str, forecast))

    return forecast_data


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет! Чтобы получить прогноз погоды на следующие три дня, отправьте мне название города.")


@bot.message_handler(func=lambda message: True)
def get_weather(message):
    city_name = message.text
    api_key = '6418b539e0697f54de8a3df65ebe9444'

    forecast = get_three_day_forecast(city_name, api_key)

    if forecast:
        response_text = ''
        for date, data in forecast:
            weather_text = (
                f"Прогноз погоды в {city_name} на {date}:\n"
                f"Температура: {data['list'][0]['main']['temp']} °C\n"
                f"Ощущается как: {data['list'][0]['main']['feels_like']} °C\n"
                f"Влажность: {data['list'][0]['main']['humidity']} %\n"
                f"Скорость ветра: {data['list'][0]['wind']['speed']} м/с\n"
                f"Описание: {data['list'][0]['weather'][0]['description']}\n\n"
            )
            response_text += weather_text
        bot.send_message(message.chat.id, response_text)
    else:
        bot.send_message(message.chat.id, "Прогноз погоды не найден. Проверьте правильность ввода.")

bot.polling()
