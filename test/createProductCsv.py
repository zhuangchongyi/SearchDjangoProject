import csv
import re

import jieba

not_exit = '~!@#$%^&*()_+{}|<>?`[]\,./~！@#￥%……&*（）——+{}|：“《》？/，。；‘【】、·'
special_product = ['中国商标注册',
                   '中国香港汇丰银行公司开户',
                   '香港汇丰银行个人开户',
                   '美国商标注册',
                   '美国公司注册',
                   '中国专利买卖']
data = [
    ["产品名称", "匹配关键字", "分值"]
]
product_names = set()
with open('templates/product_name.txt', mode='r') as file:
    product_names = sorted(set(file.read().splitlines()))

ext_stopwords = set()
with open('templates/ext_stopwords.dic', mode='r') as file:
    ext_stopwords = sorted(set(file.read().splitlines()))

jieba.load_userdict('templates/dict.dic')
for product_name in product_names:
    if product_name != '':
        keyword = set(jieba.lcut(product_name, cut_all=True))
        for key in keyword:
            if len(key) > 1 and not key in ext_stopwords and not re.match(r'^\d+$', key):
                if key in special_product:
                    data.append([product_name, key, 1.1])
                    continue
                elif key == product_name:
                    data.append([product_name, key, 1.0])
                    continue
                elif key not in not_exit and not re.match(r'^\d+$', key):
                    data.append([product_name, key, 0.1])

with open('templates/product.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
print("CSV 文件已成功输出！")
