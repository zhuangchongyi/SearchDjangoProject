import hanlp

HanLP = hanlp.pipeline() \
    .append(hanlp.utils.rules.split_sentence, output_key='sentences') \
    .append(hanlp.load('FINE_ELECTRA_SMALL_ZH'), output_key='tok') \
    .append(hanlp.load('CTB9_POS_ELECTRA_SMALL'), output_key='pos') \
    .append(hanlp.load('MSRA_NER_ELECTRA_SMALL_ZH'), output_key='ner', input_key='tok') \
    .append(hanlp.load('CTB9_DEP_ELECTRA_SMALL', conll=0), output_key='dep', input_key='tok')\
    .append(hanlp.load('CTB9_CON_ELECTRA_SMALL'), output_key='con', input_key='tok')
lp = HanLP('推荐香港开户项目暂时不需要')
print(lp)

# 加载情感分析模型
tokenizer = hanlp.load('LARGE_ALBERT_BASE')
sentiment_classifier = hanlp.load(hanlp.pretrained.sentiment_analysis.CNN_EMOTION_CLASSIFIER_ALBERT_BASE_ZH)

# 加载情感标签
sentiment_labels = ["正面", "负面"]

text = "这部电影真的很棒！"
tokens = tokenizer(text)
sentiment = sentiment_classifier.predict(tokens)
sentiment_label = sentiment_labels[sentiment[0]]

print(f"文本: {text}")
print(f"情感分类: {sentiment_label}")
