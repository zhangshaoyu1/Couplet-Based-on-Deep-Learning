from model import Model

# 配置模型参数
# 训练集输入，输出，测试集输入，输出，中文词汇表
# num_units:输出向量维度
# layers:网络层数
# dropout：防止过拟合
# batch_size：每次训练的数据集大小
# learning_rate:学习率
# restore_model:恢复模型
m = Model(
    'C:/Users/Administrator/Desktop/duilian/couplet/train/in.txt',
    'C:/Users/Administrator/Desktop/duilian/couplet/train/out.txt',
    'C:/Users/Administrator/Desktop/duilian/couplet/test/in.txt',
    'C:/Users/Administrator/Desktop/duilian/couplet/test/out.txt',
    'C:/Users/Administrator/Desktop/duilian/couplet/vocabs',
    num_units=256, layers=4, dropout=0.2,
    batch_size=16, learning_rate=0.001,
    output_dir='C:/Users/Administrator/Desktop/duilian/models/output_couplet',
    restore_model=True)

# 模型训练
m.train(100000)
