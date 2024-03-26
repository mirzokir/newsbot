MENU_CATEGORIES = [
    'Финансы 📈',
    'Игры 🕹️',
    'Новости 📰',
    'Погода ⛅'
]

MENU_FINANCE = [
    'Курс крипты ₿',
    'Новисты в бирже 📊',

]

MENU_STUDY =[
    'Новисты в оброзование',
    'Ўзбекистон Республикаси мактабгача ва мактаб таълими вазирлиги',

]



MENU_WEATHER =[
    'Прогноз погоды на день',
    'Прогноз погоды на 3 дня',

]
MENU_WEATHER_FORECAST_1_DAY = [
    'Вести город'
]
NEWS_IN_BINANCE = [

]

MENU_NEWS = [
    'ПРЕЗИДЕНТ',
    'ПРОИСШЕСТВИЯ',
    'ПОЛИТИКА',
    'ОБЩЕСТВО',
    'ЭКОНОМИКА',
    'МЫСЛИ ВСЛУХ',
    'СПОРТ',
    'КУЛЬТУРА',
]

def get_category(category_name):
    if category_name == 'ПРЕЗИДЕНТ':
        return 'president'
    elif category_name == 'ПРОИСШЕСТВИЯ':
        return 'incidents'
    elif category_name == 'ПОЛИТИКА':
        return 'policy'
    elif category_name == 'ОБЩЕСТВО':
        return 'obshestvo'
    elif category_name == 'ЭКОНОМИКА':
        return 'economy'
    elif category_name == 'МЫСЛИ ВСЛУХ':
        return 'misli'
    elif category_name == 'СПОРТ':
        return 'sport'
    elif category_name == 'КУЛЬТУРА':
        return 'culture'
