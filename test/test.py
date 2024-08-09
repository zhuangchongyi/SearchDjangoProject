import jieba
import re
#
# # 加载产品名称文件
# product_names = []
# with open("../templates/product_name.txt", 'r', encoding='utf-8') as file:
#     product_names = file.read().splitlines()
#
# ext_stopwords = []
# with open("../templates/ext_stopwords.dic", 'r', encoding='utf-8') as file:
#     ext_stopwords = file.read().splitlines()
#
# # 输入句子
# input_text = "关于中国商标注册13个地址变更的事项"
#
# # 分词并去除停用词
# stop_words = set(ext_stopwords)
# words = [word for word in jieba.lcut(input_text) if word not in stop_words]
#
# # 匹配相似产品名称
# matched_products = []
# for name in product_names:
#     name_words = [word for word in jieba.lcut(name) if word not in stop_words]
#     intersect = set(words) & set(name_words)
#     matched_products.append((name, len(intersect)))
#
# # 按照匹配数量进行排序
# matched_products.sort(key=lambda x: x[1], reverse=True)
#
# # 打印输出结果
# print(matched_products)


# 判断一个字符串是否只包含数字、字母、特殊符号等
def is_valid_string(string):
    # 定义正则表达式，匹配只包含数字、字母、特殊符号的字符串
    pattern = r'^[a-zA-Z0-9!@#$%^*&+=_ ]+$'

    # 使用re.match进行匹配
    if re.match(pattern, string.encode('unicode_escape').decode()):
        return True
    else:
        return False

# 打印输出结果
# 测试字符串
test_strings = [
    "abc123",  # 只包含字母和数字
    "Abc@123",  # 包含字母、数字和特殊符号
    "abc*&^",  # 包含字母和特殊符号
    "12345",  # 只包含数字
    "!@#$%",  # 只包含特殊符号
    "abc 123",  # 包含空格
    "abc_123",  # 包含下划线
    "＠＃￥％",  # 全角特殊符号
    "协会注册 4400+商标注册 2899=7299",  # 全角特殊符号
    "ZLNF20230828212311328"  # 全角特殊符号
]

for string in test_strings:
    print(f"{string}: {is_valid_string(string)}")