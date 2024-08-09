import re
import jieba
import json

product_name_keywords = []
ext_stopwords = set()
is_init = False


class Product:
    def __init__(self, name, keywords, score):
        self.name = name
        self.keywords = keywords
        self.score = score

    def __str__(self) -> str:
        return f"Product(name={self.name}, score={self.score}, keywords={self.keywords})"


# 判断一个字符串是否只包含数字、字母、特殊符号等
def is_valid_string(string):
    # 定义正则表达式，过滤只包含数字、字母、特殊符号的字符串
    pattern = r'^[a-zA-Z0-9!@#$%^*&+=_ ]+$'

    # 使用re.match进行匹配
    if re.match(pattern, string.encode('unicode_escape').decode()):
        return True
    else:
        return False


# 加载产品文件名称
def get_product_names():
    with open('templates/product_name.txt', 'r') as file:
        for line in file:
            line_strip = line.strip()
            line_strip_set = set(jieba.lcut_for_search(line_strip))
            line_strip_set.add(line_strip)
            product_name_keywords.append(Product(line_strip, line_strip_set, 1))


# 加载排除的名称
def get_ext_stopwords():
    with open('templates/ext_stopwords.dic', 'r') as file:
        for line in file:
            ext_stopwords.add(line.strip())


# 分词匹配产品
def get_products(input_text):
    # 字符空返回
    if len(input_text) == 0:
        return []

    # 去除数字、特殊字符
    input_text = re.sub(r'[\d_ \W]', '', input_text)

    input_text = input_text.strip()
    # 不能包含排除字符
    if input_text == '' or is_valid_string(input_text) or (input_text in ext_stopwords):
        return []

    # 分词
    words = jieba.lcut_for_search(input_text)
    # 去除停用词
    words = [word for word in words if word not in ext_stopwords]

    # 匹配相似产品名称
    matched_products = []
    for product in product_name_keywords:
        name_words = product.keywords
        intersect = set(words) & name_words
        name_words_len = len(intersect)
        if name_words_len > 0:
            _product = Product(product.name, name_words_len * product.score, intersect)
            matched_products.append(_product)

    # 按照匹配数量进行排序
    matched_products.sort(key=lambda x: x.score, reverse=True)

    # 返回
    if len(matched_products) > 5:
        return matched_products[0:5]
    # 返回
    return matched_products


# 初始化数据
get_product_names()
get_ext_stopwords()
# 加载分词字典
jieba.load_userdict("templates/ext_dict.dic")

print(get_products('关于中国商标注册13个地址变更的事项')[0])
print(get_products('协会注册 4400+商标注册 2899=7299')[0])
print(get_products('	中国商标注册')[0])
