import time
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from telebot.handler_backends import State, StatesGroup  # States

#
from telebot import TeleBot, types
from telebot.types import Message, ReplyKeyboardRemove
from configs import TOKEN
from utils import MENU_CATEGORIES, MENU_FINANCE, MENU_STUDY, MENU_NEWS, MENU_WEATHER, NEWS_IN_BINANCE, get_category
from keyboards import generate_categories, generate_button

bot = TeleBot(TOKEN, parse_mode='html')

user_data = {}


@bot.message_handler(commands=['start'])
def command_start(message: Message):
    user_id = message.from_user.id
    bot.send_message(user_id, f"Salom {message.from_user.first_name} "
                              f"o'zingizga qiziq bo'lgan bo'limni tanlang!",
                     reply_markup=generate_categories(MENU_CATEGORIES))


# --------------------------------------
@bot.message_handler(func=lambda message: message.text in MENU_NEWS)
def send_news(message: Message):
    user_id = message.from_user.id

    category_kr = message.text

    category = get_category(category_kr)
    try:
        response = requests.get(f'https://upl.uz/policy/{category}')
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        box = soup.find('div', id='dle-content')
        news = box.find_all('div', class_='short-story')
        if news is None:
            print('Xato')
        else:
            for article in news[:5]:
                title = article.find('h2', class_='sh-tit').get_text()
                description = article.find('div', 'sh-pan').get_text(strip=True)
                link = article.find('a')['href']
                image_article = 'https://upl.uz/' + article.find('img', class_='lazy-loaded')['data-src']

                time.sleep(3)

                bot.send_message(user_id,
                                 f"""Nomlanishi:{title}
l            Ta'rifi"{description}
            Link:{link}
            {image_article}
            """)
    except Exception as e:
        print("Error", e)


# --------------------------------------

@bot.message_handler(func=lambda message: message.text == 'Образование 📚')
def answer_finance(message: types.Message):
    markup = generate_categories(MENU_STUDY)
    bot.send_message(message.chat.id, text="Новисты в оброзование", reply_markup=markup)
    # Финансы---------------------------------------------------------------------------------


@bot.message_handler(func=lambda message: message.text == 'Финансы 📈')
def answer_finance(message: types.Message):
    markup = generate_categories(MENU_FINANCE)
    bot.send_message(message.chat.id, 'Финансы 📈', reply_markup=markup)


# Новости------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == 'Новости 📰')
def answer_finance(message: types.Message):
    markup = generate_categories(MENU_NEWS)
    bot.send_message(message.chat.id, 'Новисты', reply_markup=markup)


# Погода------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == 'Погода ⛅')
def answer_finance(message: types.Message):
    markup = generate_categories(MENU_WEATHER)
    bot.send_message(message.chat.id, 'Погода ⛅', reply_markup=markup)


# binance---------------------yooooordammmmmm_iskandar_aka------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == 'Курс крипты ₿')
def answer_finance(message: types.Message):
    bot.send_message(message.chat.id, )
    user_data[message.from_user.id] = {'state': 'binance'}
@bot.message_handler(commands=['Курс крипты ₿'])
def send_prices(message):
    api_url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        prices = {}

        top_20_pairs = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "SOLUSDT", "ADAUSDT",
                        "DOTUSDT", "LUNAUSDT", "LINKUSDT", "AVAXUSDT", "DOGEUSDT", "LTCUSDT",
                        "MATICUSDT", "ALGOUSDT", "ATOMUSDT", "ICPUSDT", "FILUSDT", "SHIBUSDT",
                        "UNIUSDT", "XMRUSDT"]

        for pair_data in data:
            pair = pair_data['symbol']
            if pair in top_20_pairs:
                symbol = pair.replace("USDT", "")
                prices[symbol] = float(pair_data['price'])

        response_message = ""
        for symbol, price in prices.items():
            response_message += f"{symbol}: {price}$\n"

        bot.reply_to(message, response_message)
    else:
        bot.reply_to(message, "Ошибка при запросе к API Binance")


# Новисты в бирже 📊---------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == 'Новисты в бирже 📊')
def answer_finance(message: types.Message):
    markup = generate_categories(NEWS_IN_BINANCE)
    bot.send_message(message.chat.id, 'Скоро', reply_markup=markup)


# назад---------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == '◀️назад')
def answer_finance(message: types.Message):
    chat_id = message.chat.id
    text = "Ваш текст сообщения здесь"
    bot.send_message(chat_id, text, reply_markup=generate_categories(MENU_CATEGORIES))

# Прогноз---------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == 'Прогноз погоды на день')
def answer_finance(message: types.Message):
    bot.send_message(message.chat.id, "Введите название города:")
    user_data[message.from_user.id] = {'state': 'city_name'}




# погода-------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: user_data.get(message.from_user.id) == {'state': 'city_name'})
def name_get(message):
    if message.text.strip():
        city_name = message.text.strip()
        user_data[message.from_user.id]['city_name'] = city_name
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
    else:
        bot.send_message(message.chat.id, "Siz shahar nomini kiritmadingiz. Iltimos, qaytadan kiriting.")


# ---------------------------------------------------
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


@bot.message_handler(func=lambda message: message.text == 'Прогноз погоды на 3 дня')
def answer_finance(message: types.Message):
    bot.send_message(message.chat.id, "Введите название города:")
    user_data[message.from_user.id] = {'state': 'three_day'}


@bot.message_handler(func=lambda message: user_data.get(message.from_user.id) == {'state': 'three_day'})
def name_get(message):
    if message.text.strip():
        city_name = message.text.strip()
        user_data[message.from_user.id]['three_day'] = city_name
        api_key = '6418b539e0697f54de8a3df65ebe9444'

        forecast = get_three_day_forecast(city_name, api_key)

        if forecast:
            print(forecast)
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


# ---------------------------------------------------
#         elif message.text == 'прогноз погоды на день':
#             bot.send_message(message.chat.id,bot)

bot.polling(none_stop=True)
