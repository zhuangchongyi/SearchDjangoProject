import re
from sklearn.feature_extraction.text import TfidfVectorizer

# 读取txt文件内容
with open('../templates/product_name.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 去除特殊字符和空白符
content = re.sub(r'[^\w\s]', '', content)
content = re.sub(r'\s+', ' ', content)

# 将文本内容拆分为句子列表
sentences = content.split('. ')

# 使用TF-IDF向量化器
vectorizer = TfidfVectorizer()

# 计算每个句子的TF-IDF矩阵
tfidf_matrix = vectorizer.fit_transform(sentences)

# 获取所有词汇
terms = vectorizer.get_feature_names()

# 提取关键词
keywords = []
for i in range(len(sentences)):
    sentence_keywords = [(terms[index], tfidf_matrix[i, index]) for index in tfidf_matrix[i].indices]
    sentence_keywords.sort(key=lambda x: x[1], reverse=True)  # 按权重降序排序
    keywords.extend(sentence_keywords)

# 打印关键词及权重
for keyword in keywords:
    print(keyword[0], keyword[1])
