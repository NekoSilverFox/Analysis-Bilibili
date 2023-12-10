import csv
import nltk



if __name__=="__main__":
    # 读取文件
    # with open('first50rows.csv', 'r', encoding="UTF-8") as file:
    #     contents = file.read()
    #     print(contents)
    #
    #     file.close()

    tokens_list = []
    with open('first50rows.csv', 'r', encoding="UTF-8") as file:
        csv_reader = csv.reader(file)
        # 跳过标题行
        next(csv_reader)
    #     对文本进行分词处理
        counter = 0
        for row in csv_reader:
            counter += 1
            text = row[5]
            # 把一个句子分成单词的列表
            tokens = nltk.wordpunct_tokenize(text)
            tokens_list.append(tokens)
            print(counter, "\t", text, "\t", tokens)
        file.close()

    with open('output.csv', 'w', encoding="UTF-8", newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(['tokens'])
        csv_writer.writerows([tokens] for tokens in tokens_list)
        output_file.close()




