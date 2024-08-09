import jieba
import re

product_names = set()
product_name_keywords = dict()
ext_stopwords = set()
is_init = False


class Product:
    def __init__(self, name, score, keywords):
        self.name = name
        self.score = score
        self.keywords = keywords


def init():
    if not is_init:
        # 加载分词字典
        jieba.load_userdict("templates/ext_dict.dic")


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
            product_names.add(line_strip)
            line_strip_set = set(jieba.lcut_for_search(line_strip))
            line_strip_set.add(line_strip)
            product_name_keywords.update({line_strip: line_strip_set})


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
    init()
    words = jieba.lcut_for_search(input_text)
    # 去除停用词
    words = [word for word in words if word not in ext_stopwords]

    # 匹配相似产品名称
    matched_products = []
    for name in product_name_keywords:
        name_words = product_name_keywords.get(name)
        intersect = set(words) & name_words
        name_words_len = len(intersect)
        if name_words_len > 0:
            product_dict = {}
            product_dict.update({"name": name})
            product_dict.update({"score": name_words_len})
            product_dict.update({"keywords": intersect})
            matched_products.append(product_dict)

    # 按照匹配数量进行排序
    matched_products.sort(key=lambda x: x["score"], reverse=True)

    # 返回
    if len(matched_products) > 5:
        return matched_products[0:5]
    # 返回
    return matched_products


# 初始化数据
get_product_names()
get_ext_stopwords()

print(get_products('关于中国商标注册13个地址变更的事项'))
print(get_products('协会注册 4400+商标注册 2899=7299'))
print(get_products('	中国商标注册'))
