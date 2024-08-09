import json

world_country = []
with open('templates/china_city.json') as file:
    world_country = json.load(file)

names_keywords = set()
for country in world_country:
    province = country['province']
    names_keywords.add(province)
    country_city_list = country['city']
    for country_city in country_city_list:
        city_name = country_city['name']
        if city_name != '市辖区':
            names_keywords.add(city_name)
            names_keywords.add(province + city_name)

        country_city_list = country_city['county']
        for country_city_name in country_city_list:
            if city_name != '市辖区':
                names_keywords.add(city_name + country_city_name)
                names_keywords.add(province + city_name + country_city_name)
            names_keywords.add(province + city_name + country_city_name)
            names_keywords.add(country_city_name)

with open('templates/ext_china_dict.dic', 'w', encoding='utf-8') as file:
    products = list(names_keywords)
    products.sort(key=lambda x: len(x), reverse=True)
    for product_dict in products:
        if product_dict != '':
            file.write(product_dict + '\n')
