import jieba

# 加载产品名称文件
product_names = []
with open("templates/ext_dict.dic", 'r', encoding='utf-8') as file:
    product_names = file.read().splitlines()

ext_stopwords = []
with open("templates/ext_stopwords.dic", 'r', encoding='utf-8') as file:
    ext_stopwords = file.read().splitlines()

ext_dict = set()
for ext_stopword in ext_stopwords:
    flag = False
    for product_name in product_names:
        if product_name == ext_stopword:
            flag = True
            break
    if not flag:
        ext_dict.add(ext_stopword)

ext_dicts = sorted(ext_dict, key=lambda x: (len(x), x))

ext_stopwords = []
with open('templates/ext_stopwords.dic', 'w', encoding='utf-8') as file:
    for extdict in ext_dicts:
        file.write(extdict + '\n')

print("ok")