import numpy as np
import csv
import re
import jieba
from gensim.models.word2vec import Word2Vec
from keras.models import load_model
from keras.preprocessing import sequence
from concurrent import futures
from queue import Queue
import threading
from utils.sentence_utils import read_csv_column, regex_change  # Assuming these are defined somewhere

input_file = "user_sign.csv"
output_file = "output.csv"

# 初始配置 Word2Vec 和模型
voc_dim = 150
model_word = Word2Vec.load('../model/Word2Vec.pkl')
input_dim = len(model_word.wv.key_to_index) + 1
embedding_weights = np.zeros((input_dim, voc_dim))
w2dic = {word: i + 1 for i, word in enumerate(model_word.wv.key_to_index)}
model = load_model('../model/simplifyweibo_5_moods.h5')
pchinese = re.compile('([\u4e00-\u9fa5]+)+?')

batch_size = 10000 # 每处理完这么多数据写出一次到结果文件中
num_threads = 4
progress_interval = 1000  # 每处理完这么多数据在控制台更新一次进度


def write_batch_to_csv(batch_results, output_file):
    """ 将结果写出到CSV文件的功能封装到一个函数中，每完成 batch_size 条数据处理就被调用一次 """
    with open(output_file, 'a', newline='', encoding='UTF-8') as csvfile:  # 注意：这里用'a'来追加数据
        csv_writer = csv.writer(csvfile)
        while batch_results:
            result = batch_results.pop(0)
            csv_writer.writerow(result)


def process_sentence(s):
    """ 处理单句，并返回结果 """
    s = regex_change(s)
    in_stc = ''.join(pchinese.findall(s))
    in_stc = list(jieba.cut(in_stc, cut_all=True, HMM=False))
    data = [[w2dic.get(word, 0) for word in in_stc]]
    data = sequence.pad_sequences(data, maxlen=voc_dim)
    pre = model.predict(data)[0].tolist()
    return pre


def worker(sentences, start, end, result_queue, batch_results, progress_dict, thread_id):
    """ 线程工作函数，增加进度可视化 """
    for i, s in enumerate(sentences[start:end], start=start):
        result = process_sentence(s)
        result_queue.put(result)
        # 定期将结果写入文件并更新进度
        if (i - start) % progress_interval == 0:
            progress_dict[thread_id] = i - start

            # 将队列中的数据写入到batch_results中
            while not result_queue.empty():
                batch_results.append(result_queue.get())

            if len(batch_results) >= batch_size:
                write_batch_to_csv(batch_results, output_file)
                batch_results.clear()

            # 打印进度信息
            progress_sum = sum(progress_dict.values())
            print(f"\rProgress: {progress_sum}/{len(sentences) - 113697} sentences processed.", end='')


if __name__ == '__main__':
    sentences = read_csv_column(input_file)
    result_queue = Queue()

    # 确定线程数，可以根据实际情况调整
    num_threads = 4
    futures_list = []
    range_size = len(sentences[113697:]) // num_threads
    batch_results = []  # 用于存储要写入到CSV的结果批次
    progress_dict = {i: 0 for i in range(num_threads)}  # 用于存储每个线程的进度

    with futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # 创建future到线程的映射
        future_to_thread_id = {
            executor.submit(worker, sentences, 113697 + i * range_size, 113697 + (i + 1) * range_size, result_queue,
                            batch_results, progress_dict, i): i
            for i in range(num_threads)
        }

        for future in futures.as_completed(future_to_thread_id):
            thread_id = future_to_thread_id[future]
            if future.exception() is not None:
                print(f"Thread {thread_id} generated an exception: {future.exception()}")

            # 最后，写出该线程处理的剩余结果
            while not result_queue.empty():
                batch_results.append(result_queue.get())

            write_batch_to_csv(batch_results, output_file)
            batch_results.clear()

            # 更新最终进度
            progress_dict[thread_id] = range_size if thread_id < num_threads - 1 else len(
                sentences) - 113697 - thread_id * range_size

    # 显示完成消息
    print("\nAll sentences processed.")