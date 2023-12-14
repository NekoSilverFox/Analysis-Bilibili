import numpy as np
from gensim.models.word2vec import Word2Vec
from keras.models import load_model
from keras.preprocessing import sequence
from utils.sentence_utils import *

input_file = "user_sign.csv"
output_file = "output.csv"


if __name__ == '__main__':
    voc_dim = 150
    model_word = Word2Vec.load('../model/Word2Vec.pkl') # 模型

    input_dim = len(model_word.wv.key_to_index) + 1
    embedding_weights = np.zeros((input_dim, voc_dim))
    w2dic = {}

    for i in range(len(model_word.wv.key_to_index)):
        embedding_weights[i + 1, :] = model_word.wv[list(model_word.wv.key_to_index)[i]]
        w2dic[list(model_word.wv.key_to_index)[i]] = i + 1

    model = load_model('../model/simplifyweibo_5_moods.h5')

    pchinese = re.compile('([\u4e00-\u9fa5]+)+?')

    label = {0: "生气", 1: "厌恶", 2: "快乐", 3: "喜爱", 4: "悲伤"}

    # 写出到 csv 文件中
    # with open(output_file, 'w', newline='', encoding='UTF-8') as csvfile:
    #     csv_writer = csv.writer(csvfile)
    #     # 写入 csv
    #     csv_writer.writerow()

    result_list = []
    sentences = read_csv_column(input_file)
    for s in sentences[113697 : ]:
        # print("\n原始输入：", s)
        s = regex_change(s) # 用正则表达式做清洗
        # print("正则过滤后：", s)
        in_stc = ''.join(pchinese.findall(s))
        in_stc = list(jieba.cut(in_stc, cut_all=True, HMM=False))
        new_txt = []
        data = []
        for word in in_stc:
            try:
                new_txt.append(w2dic[word])
            except:
                new_txt.append(0)
        data.append(new_txt)
        data = sequence.pad_sequences(data, maxlen=voc_dim)
        pre = model.predict(data)[0].tolist()
        result_list.append(pre)
