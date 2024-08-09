import csv
import json
import re
import threading

import jieba
import jieba.analyse
from django.http import HttpRequest

from .result import Product


# 通用工具类
class CommonUtils:

    # 获取请求参数
    @staticmethod
    def getRequestParams(request: HttpRequest):
        data = {}
        if len(request.POST) > 0:
            data.update(request.POST)
        if len(request.GET) > 0:
            data.update(request.GET)
        if len(request.body) > 0:
            text_data = request.body.decode('utf-8')
            body_json = json.loads(text_data)
            data.update(body_json)
        return data

    # 判断一个字符串是否只包含数字、字母、特殊符号等
    @staticmethod
    def is_valid_string(text: str):
        # 定义正则表达式，匹配只包含数字、字母、特殊符号的字符串
        pattern = r'^[a-zA-Z0-9!@#$%^*&+=_ ]+$'
        # 使用re.match进行匹配
        if text is not None and re.match(pattern, text.encode('unicode_escape').decode()):
            return True
        else:
            return False


# jieba分词工具类
class JiebaUtils:
    product_names: set
    ext_stopwords: set
    ext_product_names: dict
    init_state: bool = False

    def __init__(self) -> None:
        super().__init__()
        if not self.init_state:
            # 加载分词字典
            jieba.load_userdict('templates/dict.dic')
            # 初始化数据
            self.product_names = self.get_product_names()
            self.ext_stopwords = self.get_ext_stopwords()
            self.ext_product_names = self.get_products_config()
            self.init_state = True

    # 加载产品文件名称
    @staticmethod
    def get_product_names():
        product_names = set()
        with open('templates/product_name.txt', 'r') as file:
            for line in file:
                product_names.add(line.strip())
        return product_names

    # 加载过滤的句子
    @staticmethod
    def get_ext_stopwords():
        ext_stopwords = set()
        with open('templates/ext_stopwords.dic', 'r') as file:
            for line in file:
                ext_stopwords.add(line.strip())
        return ext_stopwords

    # 读取csv文件的产品配置数据
    @staticmethod
    def get_products_config():
        ext_product_names = {}
        with open('templates/product.csv', mode='r') as file:
            reader = csv.reader(file)
            # 跳过标题行
            next(reader)
            # 封装数据
            for row in reader:
                # 产品
                row_0 = row[0]
                # 匹配关键词
                row_1 = row[1]
                # 匹配分值
                row_2 = row[2]
                get_product = ext_product_names.get(row_0)
                product_dict = Product(row_1, float(row_2))
                if get_product is None:
                    ext_product_names.update({row_0: [product_dict]})
                else:
                    get_product.append(product_dict)
        return ext_product_names

    # 合并关键字，计算匹配相似度
    @staticmethod
    def get_montage_words(montage_list: set, product_name: str):
        montage_list = sorted(montage_list, key=lambda x: len(x), reverse=True)
        product_name_length = len(product_name)
        # 基数
        base_score = 0.10
        # 按照匹配比例计算
        for join_text in montage_list:
            join_score = len(join_text) / product_name_length
            if product_name == join_text:
                base_score += 0.50 * join_score
            if product_name.startswith(join_text) or product_name.endswith(join_text):
                base_score += 0.20 * join_score
            elif join_text in product_name:
                base_score += 0.10 * join_score
        return base_score

        # 生成组合

    @staticmethod
    def get_combination_words(characters):
        combinations = []

        def backtrack(curr_combination, remaining_chars):
            # 添加当前组合到结果列表
            if curr_combination != '':
                combinations.append(curr_combination)
            for char in remaining_chars:
                new_remaining = [c for c in remaining_chars if c != char]
                # 递归调用 backtrack，加上当前字符作为新的组合
                backtrack(curr_combination + char, new_remaining)

        backtrack('', characters)
        # for r in range(1, len(characters) + 1):
        #     itertools_combinations = list(itertools.combinations(characters, r))
        #     combination_word = ""
        #     for combination in itertools_combinations:
        #         combination_word += "".join(combination)
        #     combinations.append(combination_word)
        return combinations

    # 分词匹配产品
    def search_product_1(self, input_text: str):
        # 不能包含排除字符
        if CommonUtils.is_valid_string(input_text) or (input_text in self.ext_stopwords):
            return []
        # 分词
        words = jieba.lcut_for_search(input_text)
        # 去除停用词
        words = [word for word in words if word not in self.ext_stopwords]
        # 匹配相似产品名称
        matched_products = []
        for name in self.product_names:
            name_words = jieba.lcut_for_search(name)
            intersect = set(words) & set(name_words)
            if len(intersect) > 1:
                matched_products.append((name, len(intersect)))
        # 按照匹配数量进行排序
        matched_products.sort(key=lambda x: x[1], reverse=True)
        return matched_products

    # 搜索匹配产品
    def search_product_2(self, input_text: str):
        # 返回结果
        matched_products = []
        # 不能包含排除字符
        if CommonUtils.is_valid_string(input_text) or (input_text in self.ext_stopwords):
            return matched_products
        # 分词、去除停用词
        words = set(word for word in jieba.lcut(input_text, cut_all=True)
                    if len(word) > 1 and not re.match(r"[^\w\s]+", word)
                    and word not in self.ext_stopwords)
        # 使用TF-IDF提取关键词及权重
        input_text_tf_idf = jieba.analyse.extract_tags(input_text, topK=None, withWeight=True)
        words = words.union(set(tf_idf[0] for tf_idf in input_text_tf_idf
                                if len(tf_idf[0]) > 1 and not re.match(r"[^\w\s]+", tf_idf[0])
                                and tf_idf[0] not in self.ext_stopwords))
        # 匹配产品
        for product_name in self.ext_product_names:
            self.process_data(product_name, words, input_text_tf_idf, matched_products)

        matched_products.sort(key=lambda product: product.score, reverse=True)
        return matched_products

    # 搜索匹配产品
    def search_product(self, input_text: str):
        # 返回结果
        matched_products = []
        # 不能包含排除字符
        if CommonUtils.is_valid_string(input_text) or (input_text in self.ext_stopwords):
            return matched_products
        # 分词、去除停用词
        words = set(word for word in jieba.lcut(input_text, cut_all=True)
                    if len(word) > 1 and not re.match(r"[^\w\s]+", word)
                    and word not in self.ext_stopwords)
        # 使用TF-IDF提取关键词及权重
        input_text_tf_idf = jieba.analyse.extract_tags(input_text, topK=None, withWeight=True)
        words = words.union(set(tf_idf[0] for tf_idf in input_text_tf_idf
                                if len(tf_idf[0]) > 1 and not re.match(r"[^\w\s]+", tf_idf[0])
                                and tf_idf[0] not in self.ext_stopwords))
        # 创建线程列表
        threads = []
        # 匹配产品
        for product_name in self.ext_product_names:
            # self.process_data(product_name, words, input_text_tf_idf, matched_products)
            # 创建线程，并将要处理的数据作为参数传递给线程函数
            thread = threading.Thread(target=self.process_data,
                                      args=(product_name, words, input_text_tf_idf, matched_products))
            # 启动线程
            thread.start()
            # 将线程添加到列表中
            threads.append(thread)

        # 等待所有线程完成
        for thread in threads:
            thread.join()
        # 排序
        matched_products.sort(key=lambda product: product.score, reverse=True)
        return matched_products

    def process_data(self, product_name, words, input_text_tf_idf, matched_products):
        ext_product_name_get = self.ext_product_names.get(product_name)
        product_name_set = set(product.name for product in ext_product_name_get)
        intersect_words = words & product_name_set
        # 计算分值，匹配命中个数大于1
        intersect_num = len(intersect_words)
        if intersect_num > 1:
            combination_words = self.get_combination_words(intersect_words)
            permutation_word_list = intersect_words.union(
                set(join_word for join_word in combination_words if join_word in product_name))
            tf_idf_sum_score = sum(tf_idf[1] for tf_idf in input_text_tf_idf if
                                   tf_idf[0] in product_name or tf_idf[0] in permutation_word_list)
            if tf_idf_sum_score > 0:
                product_sum_score = (
                        sum(product.score for product in ext_product_name_get if product.name in intersect_words)
                        + sum(product.score for product in ext_product_name_get if product.name == product_name))
                montage_word_score = self.get_montage_words(permutation_word_list, product_name)
                # 调整分值计算方式(关键词权重和 * 自定义关键词权重和 * 匹配相似度)
                score = tf_idf_sum_score * product_sum_score * montage_word_score
                if score > 0.5:
                    matched_products.append(Product(product_name, score))
