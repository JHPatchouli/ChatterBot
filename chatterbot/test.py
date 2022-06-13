import codecs
import os
import re
import jieba

bigram_pairs = []

stopword = []
for line in codecs.open(os.path.dirname(__file__) + '/data/cn_stopwords.txt', 'rb', 'utf-8'):
    for word in line.split():
        stopword.append(word)
jieba.load_userdict(os.path.dirname(__file__) + '/data/user_dict.txt')

text="这个牛逼那个傻逼"
# 利用正则表达式去掉一些一些标点符号之类的符号。
text = re.sub(r'\s+', ' ', str(text))  # trans 多空格 to空格
text = re.sub(r'\n+', ' ', str(text))  # trans 换行 to空格
text = re.sub(r'\t+', ' ', str(text))  # trans Tab to空格
text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——；！，”。《》，。：“？、~@#￥%……&*（）1234567①②③④)]+".encode().decode("utf8"), "".encode().decode("utf8"), text)

wordlist = list(jieba.cut(str(text)))  # jieba.cut  把字符串切割成词并添加至一个列表

for word in wordlist:
    if word not in stopword:  # 词语的清洗：去停用词
        if word != '\r\n' and word != ' ' and word != '\u3000'.encode().decode('unicode_escape') \
                and word != '\xa0'.encode().decode('unicode_escape'):  # 词语的清洗：去全角空格
            bigram_pairs.append(word)
