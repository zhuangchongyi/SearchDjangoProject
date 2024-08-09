import spacy
from sklearn.metrics.pairwise import cosine_similarity

class ProductMatcher:
    def __init__(self):
        self.product_names = []  # 存储所有产品名称的列表
        self.nlp = spacy.load("zh_core_web_sm")  # 加载词向量模型

    def add_product(self, product_name):
        self.product_names.append(product_name)

    def match_product(self, user_input):
        user_doc = self.nlp(user_input.lower())  # 将用户输入转换为词向量表示
        max_similarity = -1
        matched_product = None
        for product_name in self.product_names:
            product_doc = self.nlp(product_name.lower())  # 将产品名转换为词向量表示
            similarity = cosine_similarity([user_doc.vector], [product_doc.vector])[0][0]
            if similarity > max_similarity:
                max_similarity = similarity
                matched_product = product_name
        return matched_product

# 创建ProductMatcher对象
product_matcher = ProductMatcher()

# 添加产品名称到产品库
product_matcher.add_product("中国商标注册")
product_matcher.add_product("英国商标注册")
product_matcher.add_product("美国商标注册")
product_matcher.add_product("德国商标注册")

# 用户输入
user_input = "注册中国商标"

# 匹配产品
matched_product = product_matcher.match_product(user_input)
if matched_product:
    print(f"匹配的产品：{matched_product}")
else:
    print("未找到匹配的产品")
