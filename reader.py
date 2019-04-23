from queue import Queue
import random


def padding_seq(seq):
    results = []
    max_len = 0
    for s in seq:
        if max_len < len(s):
            max_len = len(s)
    for i in range(0, len(seq)):
        l = max_len - len(seq[i])
        results.append(seq[i] + [0 for j in range(l)])
    return results


def encode_text(words, vocab_indices):
    return [vocab_indices[word] for word in words if word in vocab_indices]


def decode_text(labels, vocabs, end_token='</s>'):
    results = []
    for idx in labels:
        word = vocabs[idx]
        if word == end_token:
            return ' '.join(results)
        results.append(word)
    return ' '.join(results)


# 读取词表文件
def read_vocab(vocab_file):
    f = open(vocab_file, 'rb')
    vocabs = [line.decode('utf8')[:-1] for line in f]
    f.close()
    return vocabs


class SeqReader():
    # 配置参数并初始化文件读取
    def __init__(self, input_file, target_file, vocab_file, batch_size,
                 queue_size=2048, worker_size=2, end_token='</s>',
                 padding=True, max_len=50):
        self.input_file = input_file  # 训练集输入
        self.target_file = target_file  # 训练集输出
        self.end_token = end_token  # 文件结束标志
        self.batch_size = batch_size  # 每次数据集大小
        self.padding = padding  # 填充
        self.max_len = max_len  # 最大长度
        # self.vocabs = read_vocab(vocab_file) + [end_token]
        self.vocabs = read_vocab(vocab_file)  # 读取词表文件存到变量vocabs列表中
        self.vocab_indices = dict((c, i) for i, c in enumerate(self.vocabs))  # 枚举及标号vocabs存入字典中
        self.data_queue = Queue(queue_size)  # 数据队列
        self.worker_size = worker_size
        with open(self.input_file, 'rb') as f:
            for i, l in enumerate(f):
                pass
            f.close()
            self.single_lines = i + 1
        self.data_size = int(self.single_lines / batch_size)
        self.data_pos = 0
        self._init_reader()

    def start(self):
        return

    '''
        for i in range(self.worker_size):
            t = Thread(target=self._init_reader())
            t.daemon = True
            t.start()
    '''

    # 读取一条对联
    def read_single_data(self):
        if self.data_pos >= len(self.data):
            random.shuffle(self.data)
            self.data_pos = 0
        result = self.data[self.data_pos]
        self.data_pos += 1
        return result

    # 读取n条对联
    def read(self):
        while True:
            batch = {'in_seq': [],
                     'in_seq_len': [],
                     'target_seq': [],
                     'target_seq_len': []}
            for i in range(0, self.batch_size):  # 添加n对对联数据
                item = self.read_single_data()  # 获取一条对联
                batch['in_seq'].append(item['in_seq'])
                batch['in_seq_len'].append(item['in_seq_len'])
                batch['target_seq'].append(item['target_seq'])
                batch['target_seq_len'].append(item['target_seq_len'])
            if self.padding:  # 填充
                batch['in_seq'] = padding_seq(batch['in_seq'])
                batch['target_seq'] = padding_seq(batch['target_seq'])
            yield batch

    # 初始化文件读取，将训练集读取，处理，存入data列表
    def _init_reader(self):
        self.data = []
        input_f = open(self.input_file, 'rb')
        target_f = open(self.target_file, 'rb')
        for input_line in input_f:
            input_line = input_line.decode('utf-8')[:-1]  # 上联
            input_words = [x for x in input_line.split(' ') if x != '']  # 上联包含的汉字列表
            if len(input_words) >= self.max_len:  # 如果上联太长，缩短
                input_words = input_words[:self.max_len - 1]
            input_words.append(self.end_token)  # 增加结束标志

            target_line = target_f.readline().decode('utf-8')[:-1]  # 对应下联
            target_words = [x for x in target_line.split(' ') if x != '']  # 下联包含的汉字列表
            if len(target_words) >= self.max_len:  # 如果下联太长，缩短
                target_words = target_words[:self.max_len - 1]
            target_words = ['<s>', ] + target_words
            target_words.append(self.end_token)

            in_seq = encode_text(input_words, self.vocab_indices)  # 获取上联各字在字典中的位置
            target_seq = encode_text(target_words, self.vocab_indices)  # 获取下联各字在字典中的位置
            self.data.append({  # 添加一条对联记录
                'in_seq': in_seq,
                'in_seq_len': len(in_seq),
                'target_seq': target_seq,
                'target_seq_len': len(target_seq) - 1
            })
        input_f.close()
        target_f.close()
        self.data_pos = len(self.data)
