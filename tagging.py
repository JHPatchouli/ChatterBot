import imp
import os
import string
from chatterbot import languages
import jieba
import re
import codecs


class LowercaseTagger(object):
    """
    Returns the text in lowercase.
    """

    def __init__(self, language=None):
        self.language = language or languages.ENG

    def get_text_index_string(self, text):
        return text.lower()

    def get_bigram_pair_string(self, text):
        return text.lower()


class PosLemmaTagger(object):

    def __init__(self, language=None):
        import spacy
        self.language = language or languages.ENG

        self.punctuation_table = str.maketrans(
            dict.fromkeys(string.punctuation))
        if self.language.ISO_639_1.lower() == 'en':
            self.nlp = spacy.load('en_core_web_sm')
        else:
            self.nlp = spacy.load(self.language.ISO_639_1.lower())

    def get_text_index_string(self, text):
        """
        Return a string of text containing part-of-speech, lemma pairs.
        """
        bigram_pairs = []

        if len(text) <= 2:
            text_without_punctuation = text.translate(self.punctuation_table)
            if len(text_without_punctuation) >= 1:
                text = text_without_punctuation

        document = self.nlp(text)

        if len(text) <= 2:
            bigram_pairs = [
                token.lemma_.lower() for token in document
            ]
        else:
            tokens = [
                token for token in document if token.is_alpha and not token.is_stop
            ]

            if len(tokens) < 2:
                tokens = [
                    token for token in document if token.is_alpha
                ]

            for index in range(1, len(tokens)):
                bigram_pairs.append('{}:{}'.format(
                    tokens[index - 1].pos_,
                    tokens[index].lemma_.lower()
                ))

        if not bigram_pairs:
            bigram_pairs = [
                token.lemma_.lower() for token in document
            ]

        return ' '.join(bigram_pairs)

    def get_bigram_pair_string(self, text):
        """
        Return a string of text containing part-of-speech, lemma pairs.
        """
        bigram_pairs = []

        stopword = []
        for line in codecs.open(os.path.dirname(__file__) + '/data/cn_stopwords.txt', 'rb', 'utf-8'):
            for word in line.split():
                stopword.append(word)

        #jieba.load_userdict(os.path.dirname(__file__) + '/data/user_dict.txt')

        # 利用正则表达式去掉一些一些标点符号之类的符号。
        text = re.sub(r'\s+', ' ', str(text))  # trans 多空格 to空格
        text = re.sub(r'\n+', ' ', str(text))  # trans 换行 to空格
        text = re.sub(r'\t+', ' ', str(text))  # trans Tab to空格
        text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——；！，”。《》，。：“？、~@#￥%……&*（）1234567①②③④)]+".
                      encode().decode("utf8"), "".encode().decode("utf8"), text)

        wordlist = list(jieba.cut(str(text)))  # jieba.cut  把字符串切割成词并添加至一个列表
        for word in wordlist:
            if word not in stopword:  # 词语的清洗：去停用词
                if word != '\r\n' and word != ' ' and word != '\u3000'.encode().decode('unicode_escape') \
                        and word != '\xa0'.encode().decode('unicode_escape'):  # 词语的清洗：去全角空格
                    bigram_pairs.append(word)

        return ' '.join(bigram_pairs)
