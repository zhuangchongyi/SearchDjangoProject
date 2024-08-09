import jieba
import re


# 判断一个字符串是否只包含数字、字母、特殊符号等
def is_valid_string(string):
    # 定义正则表达式，过滤只包含数字、字母、特殊符号的字符串
    pattern = r'^[0-9!@#$%^*&+=_ ]+$'

    # 使用re.match进行匹配
    if re.match(pattern, string.encode('unicode_escape').decode()):
        return True
    else:
        return False


# 加载产品名称文件
product_names = []
invalid_keywords = ['（', '）', '(', ')', '【', '】', '[', ']']
with open("templates/product_name.txt", 'r', encoding='utf-8') as file:
    product_names = file.read().splitlines()

jieba.load_userdict("templates/dict.dic")

product_names_keywords = []
for product_name in set(product_names):
    if product_name != '':
        keyword_set = set()
        keywords = jieba.lcut_for_search(product_name)
        for keyword in set(keywords):
            # if not is_valid_string(keyword) and (not keyword in invalid_keywords):
            if not keyword in invalid_keywords:
                keyword_set.add(keyword)

        if len(keyword_set) > 0:
            keyword_set = sorted(keyword_set, key=lambda x: (len(x), x))
            keyword = product_name + '##' + ','.join(keyword_set)
            product_names_keywords.append(keyword)

# with open('templates/product_dict.dic', 'w', encoding='utf-8') as file:
#     for product_dict in sorted(product_names_keywords):
#         file.write(product_dict + '\n')

print("ok")
