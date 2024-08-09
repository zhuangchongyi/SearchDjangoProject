import jieba

product_names = set()
ext_stopwords = set()
product_names_words = []


# 加载产品文件名称
def get_product_names():
    with open('templates/product_name.txt', 'r') as file:
        for line in file:
            product_names.add(line.strip())
            product_names_words.append(jieba.lcut_for_search(line.strip()))


# 输入句子分词
def tokenize_input_text(input_text):
    return jieba.lcut_for_search(input_text.strip())


# 分词匹配产品
def get_products(input_text):
    # 分词
    words = tokenize_input_text(input_text)

    # 去除停用词
    words = [word for word in words if word not in ext_stopwords]

    # 匹配相似产品名称
    matched_products = []
    for name, name_words in zip(product_names, product_names_words):
        intersect = set(words) & set(name_words)
        if len(intersect) > 0:
            matched_products.append((name, len(intersect)))

    # 按照匹配数量进行排序
    matched_products.sort(key=lambda x: x[1], reverse=True)

    # 连续高匹配数量的放在前面
    sorted_matched_products = []
    max_score = matched_products[0][1]
    for product, score in matched_products:
        if score == max_score:
            sorted_matched_products.insert(0, (product, score))
        else:
            sorted_matched_products.append((product, score))

    if len(matched_products) > 10:
        return matched_products[0:10]
    return matched_products


# 加载排除的名称
def get_ext_stopwords():
    with open('templates/ext_stopwords.dic', 'r') as file:
        for line in file:
            ext_stopwords.add(line.strip())


# 加载分词字典
jieba.load_userdict("templates/ext_dict.dic")
# 初始化数据
get_product_names()
get_ext_stopwords()

print(get_products('关于中国商标注册13个地址变更的事项'))
