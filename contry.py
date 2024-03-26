from countryinfo import CountryInfo
from pprint import pprint
import json

while True:
    country_name = input('Davlat nomini kiriting (english): ')
    if country_name == 'stop':
        pprint('Dastur toxtadi')
        break
    try:
        get_country = CountryInfo(country_name)
        data = get_country.info()
        pprint(data)

        name = data['name']
        area = data['area']
        capital = data['capital']
        population = data['population']
        currencies = data['currencies']
        languages = data['languages']
        region = data['region']

        print(f"""{name} davlat haqidago ma'lumot:
{name} davlat {region} qit'asida joylashgan!
Uning hududi: {area} kv.km
Poytaxti: {capital} shaxri!
Axoli soni: {population} ga yetdi!
Qabul qilingan tillar: {languages} !
Pul birligi: {currencies} 
""")



    except Exception:
        pprint('Siz natogri davlat kiritingiz!')