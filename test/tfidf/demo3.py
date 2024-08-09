import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# 读取txt文件内容
with open('product_reviews.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 去除特殊字符和空白符
content = re.sub(r'[^\w\s]', '', content)
content = re.sub(r'\s+', ' ', content)

# 将文本内容拆分为句子列表并进行标记（正面或负面）
sentences = [sentence.split('\t') for sentence in content.split('. ')]

# 使用TF-IDF向量化器
vectorizer = TfidfVectorizer()

# 提取句子中的关键词，并将其转换为特征向量
X = []
y = []
for sentence in sentences:
    keywords = ' '.join(sentence[0].split())  # 将关键词连接成一个字符串
    X.append(keywords)
    y.append(sentence[1])

X = vectorizer.fit_transform(X)

# 构建分类模型
model = LogisticRegression()
model.fit(X, y)

# 预测情感倾向
input_text = "这个产品功能强大，性价比高"
keywords = ' '.join([term for term in input_text.split() if term in vectorizer.get_feature_names()])
X_input = vectorizer.transform([keywords])
sentiment = model.predict(X_input)[0]

if sentiment == 'positive':
    print("情感倾向：正面")
else:
    print("情感倾向：负面")
