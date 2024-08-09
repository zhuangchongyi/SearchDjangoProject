import re

import jieba

# 加载产品名称文件
product_name_list = []
ext_dict = []
ext_stopwords = []
ext_china_dict = []
ext_world_dict = []
ext_dict_en = []

with open("templates/product_name.txt", 'r', encoding='utf-8') as file:
    product_name_list = file.read().splitlines()

with open("templates/ext_stopwords.dic", 'r', encoding='utf-8') as file:
    ext_stopwords = file.read().splitlines()

with open("templates/ext_dict.dic", 'r', encoding='utf-8') as file:
    ext_dict = file.read().splitlines()

with open("templates/ext_china_dict.dic", 'r', encoding='utf-8') as file:
    ext_china_dict = file.read().splitlines()

with open("templates/ext_world_dict.dic", 'r', encoding='utf-8') as file:
    ext_world_dict = file.read().splitlines()

with open("templates/ext_dict_en.dic", 'r', encoding='utf-8') as file:
    ext_dict_en = file.read().splitlines()

# 设置初始化字典
dict_word_list = product_name_list + ext_dict + ext_china_dict + ext_world_dict + ext_dict_en
with open('templates/dict.dic', 'w', encoding='utf-8') as file:
    for product_dict in set(dict_word_list):
        if product_dict != '':
            file.write(product_dict + '\n')

# 产品分词生成字典
jieba.load_userdict("templates/dict.dic")
invalid_keywords = '~!@#$%^&*()_+{}|<>?`[]\,./~！@#￥%……&*（）——+{}|：“《》？/，。；‘【】、·'
product_names_keywords = []
for product_name in set(product_name_list):
    if product_name != '':
        keywords = jieba.lcut(product_name, cut_all=True)
        product_names_keywords.append(product_name)
        for keyword in set(keywords):
            if (len(keyword) > 1
                    and not re.match(r'^\d+$', keyword)
                    and not keyword in invalid_keywords
                    and not keyword in ext_stopwords):
                product_names_keywords.append(keyword)

product_names_keywords += dict_word_list
with open('templates/dict.dic', 'w', encoding='utf-8') as file:
    products = list(set(product_names_keywords))
    product_names_keywords = sorted(products, key=lambda x: len(x), reverse=True)
    for product_dict in product_names_keywords:
        file.write(product_dict + '\n')

# with open('templates/ext_dict_en.dic', 'w', encoding='utf-8') as file:
#     pattern = re.compile(r'[\u4e00-\u9fff]')  # 匹配 Unicode 范围内的中文字符
#     for product_dict in product_names_keywords:
#         if len(product_dict) > 1 and not bool(pattern.search(product_dict)):
#             file.write(product_dict + '\n')

print("ok")
