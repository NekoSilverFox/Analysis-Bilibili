"""
@Data: 11.25.2023
@Author: Li Yijia
"""
import csv
import re
from typing import List
from collections import Counter
import jieba
import pandas as pd
from wordcloud import wordcloud
import nltk

# 输入输出文件信息
origanal_csv_file = '../../Analysis-Bilibili/src/sentiment_analysis/user_sign.csv'
stopword_file = '../../Analysis-Bilibili/src/sentiment_analysis/baidu_stopwords.txt'
word_freq_output_csv_file = 'word-freq-output.csv'


def read_csv_column(process_file, col_num=0) -> List:
    """ 从csv文件读取一列，转化成List. """
    records_list = []
    with open(process_file, 'r', encoding="UTF-8") as file:
        csv_reader = csv.reader(file)
        # next(csv_reader) # 跳过标题行
        #     对文本进行分词处理
        counter = 0
        for row in csv_reader:
            counter += 1
            text = row[col_num].rstrip('\n')
            if text:
                records_list.append(text)
        file.close()
    return records_list

def get_stopword_list(file):
    """ 读取停用词表 """
    with open(file, 'r', encoding='UTF-8') as f:
        stopword_list = [word.strip('\n') for word in f.readlines()]
    return stopword_list


# def sent2word(sentence):
#     """
#     文本切割
#     Segment a sentence to words
#     Delete stopwords
#     """
#     segList = jieba.cut(sentence)
#     segResult = []
#     for w in segList:
#         segResult.append(w)
#
#     stopwords = get_stopword_list("baidu_stopwords.txt")
#     newSent = []
#     for word in segResult:
#         if word in stopwords:
#             # print "stopword: %s" % word
#             continue
#         else:
#             newSent.append(word)
#     return newSent

def sentenses2words(lines, stopwords):
    """ 使用正则过滤，去除停用词，并返回词袋字典和所有词. """
    stopwords = get_stopword_list(stopword_file)
    all_words = []
    for line in lines:
        line = regex_change(line)
        all_words += [word for word in jieba.cut(line) if word not in stopwords]

    return all_words


def regex_change(line):
    """ 对没用的字符进行过滤删除，包括特殊字符、符号等. """
    # 前缀的正则
    username_regex = re.compile(r"^\d+::")
    # URL，为了防止对中文的过滤，所以使用[a-zA-Z0-9]而不是\w
    url_regex = re.compile(r"""(https?://)?([a-zA-Z0-9]+)(\.[a-zA-Z0-9]+)+(/[a-zA-Z0-9]*)*""",
                           re.VERBOSE | re.IGNORECASE)
    # 剔除用户名和邮箱地址
    user_email_regex = re.compile(r"\S*@\S*\s?")
    # 剔除日期
    date_regex = re.compile(u"""年|月|日|(周一)|(周二)|周三|周四|周五|周六""", re.VERBOSE)
    # 剔除所有数字（含带前缀后缀的）
    decimal_regex = re.compile(r'[^a-zA-Z]\d+')
    # 剔除单独的、前后带符号的数字，不包括中文数字
    standalone_decimal_regex = re.compile(r'\b\d+\b')
    # 剔除标点符号、特殊字符
    punctuation_regex = re.compile(r"[^\w\s]|_")
    # 剔除空格（包括全角空格）
    space_regex = re.compile(r"\s+|　+")
    # 剔除日语平假名和片假名
    japan_regex = re.compile(r"[ぁ-んァ-ン]")

    line = username_regex.sub("", line)
    line = url_regex.sub("", line)
    line = user_email_regex.sub("", line)
    line = date_regex.sub("", line)
    line = decimal_regex.sub("", line)
    line = standalone_decimal_regex.sub("", line)
    line = punctuation_regex.sub("", line)
    line = space_regex.sub("", line)
    line = japan_regex.sub("", line)
    return line

def extract_from_csv(file, given_nrows):
    # 设置显示的最大行和列数，以免显示不全
    pd.options.display.max_rows = 15
    pd.options.display.max_columns = 15
    # 读取前500条记录，假定第一行为header
    df = pd.read_csv(file, nrows=given_nrows)
    # 将前500条记录保存到新的CSV文件中
    df.to_csv("extracted.csv", index=False)

