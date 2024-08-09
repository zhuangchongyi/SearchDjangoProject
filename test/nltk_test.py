import nltk
import jieba
from pyhanlp import *
from textblob import TextBlob


def def1(text):
    tokens = nltk.word_tokenize(text)
    return tokens


def def2(text):
    jieba.load_userdict('templates/dict.dic')
    tokens = jieba.lcut(text)
    return tokens


def def3(text):
    # 演示中文分词
    segmenter = HanLP.newSegment().enableCustomDictionary(False)
    word_list = segmenter.seg(text)
    # print(word_list)

    # 演示中文词性标注
    # tagger = PerceptronLexicalAnalyzer()  # 可以使用感知机词法分析器
    # result = tagger.analyze(text)
    # for word in result.iterator():
    #     print("%s\t%s" % (word.value, word.label))

    words = []
    for word in word_list:
        words.append([str(word.word), str(word.nature)])
    return words

def def4(text):
    blob = TextBlob(text)
    sentiment_polarity = blob.sentiment.polarity
    return sentiment_polarity


input_text = '这部电影真的很棒！'
# def_text = def1(input_text)
# print(def_text)

# def_text = def2(input_text)
# print(def_text)

# def_text = def3(input_text)
# print(def_text)


def_text = def4(input_text)
print(def_text)

