import requests
import telebot
from datetime import datetime, timedelta

TOKEN = '6762831128:AAF-2aCsxx2APxfguirpxugi6LDZKr1QNAg'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет! Напиши 'прогноз погоды на день', чтобы узнать прогноз погоды на следующий день.")


@bot.message_handler(func=lambda message: message.text == 'прогноз погоды на день')
def ask_city(message):
    bot.send_message(message.chat.id, "Введите название города:")


@bot.message_handler(func=lambda message: True)
def get_weather(message):
    if message.text == 'прогноз погоды на день':
        bot.send_message(message.chat.id, "Введите название города:")
    else:
        city_name = message.text
        api_key = "6418b539e0697f54de8a3df65ebe9444"

        tomorrow_date = datetime.now() + timedelta(days=1)
        tomorrow_date_str = tomorrow_date.strftime('%Y-%m-%d')

        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric"
        response = requests.get(url)
        forecast_data = response.json()

        if 'list' in forecast_data:
            forecast_list = forecast_data['list']
            tomorrow_forecast = None
            for forecast in forecast_list:
                forecast_date = forecast['dt_txt'].split()[0]
                if forecast_date == tomorrow_date_str:
                    tomorrow_forecast = forecast
                    break

            if tomorrow_forecast:
                weather_text = (
                    f"Прогноз погоды в {city_name} на {tomorrow_date_str}:\n"
                    f"Температура: {tomorrow_forecast['main']['temp']} °C\n"
                    f"Ощущается как: {tomorrow_forecast['main']['feels_like']} °C\n"
                    f"Скорость ветра: {tomorrow_forecast['wind']['speed']} м/с\n"
                    f"Влажность: {tomorrow_forecast['main']['humidity']} %\n"
                    f"Давление: {tomorrow_forecast['main']['pressure']} гПа"
                )
                bot.send_message(message.chat.id, weather_text)
            else:
                bot.send_message(message.chat.id, "Прогноз погоды на следующий день не найден.")
        else:
            bot.send_message(message.chat.id, "Прогноз погоды не найден. Проверьте правильность ввода.")

bot.polling()
