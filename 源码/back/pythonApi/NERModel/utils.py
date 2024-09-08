import logging
import os
import sys
import torch
import pickle

from torch.utils.data import TensorDataset
from tqdm import tqdm

logger = logging.getLogger(__name__)

class InputExample(object):
    """A single training/test example for simple sequence classification."""
    def __init__(self, guid, text, label=None):
        self.guid = guid  # 句子唯一标识符
        self.text = text # 文本
        self.label = label # 标签

class InputFeatures(object):
    """A single set of features of data."""
    def __init__(self, input_ids, input_mask, segment_ids, label_id, ori_tokens):
        self.input_ids = input_ids  # 输入的id
        self.input_mask = input_mask # 输入的掩码 表示有效位
        self.segment_ids = segment_ids # 段落标识符
        self.label_id = label_id   # 标签标识符
        self.ori_tokens = ori_tokens  # 原始词语

class NerProcessor(object):
    def read_data(self, input_file):
        """
            从文件中读取 BIO(Beginning, Inside, Outside)格式的数据
            这个函数会将输入文件中的 BIO 格式数据进行解析和整理，将相邻的词语和标签组合在一起，形成更加易于处理的数据行。
            函数返回一个列表，其中每个元素都是一个列表，包含一个标签序列和一个词语序列。
        """
        with open(input_file, "r", encoding="utf-8") as f:
            lines = []  # 存储处理后的数据行
            words = []  # 存储当前行的词语
            labels = []  # 存储当前行的标签

            for line in f.readlines():   
                # 去除行两端的空白字符
                contends = line.strip()
                # 将行按空格分割成词语和标签
                tokens = line.strip().split(" ")

                if len(tokens) == 2:
                    # 当行包含两个词语和标签时，将它们分别存储到words和labels列表中
                    words.append(tokens[0])
                    labels.append(tokens[1])
                else:
                    # 当行为空行并且之前存在的词语和标签不为空时
                    if len(contends) == 0 and len(words) > 0:
                        label = []
                        word = []
                        # 将每个词语和标签组合，添加到lines列表中
                        for l, w in zip(labels, words):
                            if len(l) > 0 and len(w) > 0:
                                label.append(l)
                                word.append(w)
                        lines.append([' '.join(label), ' '.join(word)])
                        words = []
                        labels = []  
            return lines
    def get_labels(self, args):
        labels = set()  # 存储标签集合
        if os.path.exists(os.path.join(args.output_dir, "label_list.pkl")):
            # 如果已经存在存储的标签文件，从中加载标签集合
            logger.info(f"loading labels info from {args.output_dir}")
            with open(os.path.join(args.output_dir, "label_list.pkl"), "rb") as f:
                labels = pickle.load(f)
        else:
            # 从训练数据中获取标签
            logger.info(f"loading labels info from train file and dump in {args.output_dir}")
            with open(args.train_file,'r',encoding='utf-8') as f:
                for line in f.readlines():
                    tokens = line.strip().split(" ")
                    if len(tokens) == 2:
                        labels.add(tokens[1])

            if len(labels) > 0:
                # 如果成功获取了标签，将它们保存到文件中
                with open(os.path.join(args.output_dir, "label_list.pkl"), "wb") as f:
                    pickle.dump(labels, f)
            else:
                # 如果无法获取标签，返回默认的标签集合
                logger.info("loading error and return the default labels B,I,O")
                labels = {"O", "B", "I"}

        return labels  # 返回标签集合
    
    def get_examples(self, input_file):
        examples = []  # 存储示例的列表
        
        lines = self.read_data(input_file)  # 调用 read_data 函数读取处理后的数据行

        for i, line in enumerate(lines):
            guid = str(i)  # 示例的唯一标识符，这里使用行号
            text = line[1]  # 示例的文本内容
            label = line[0]  # 示例的标签序列

            # 创建一个 InputExample 对象并添加到 examples 列表中
            examples.append(InputExample(guid=guid, text=text, label=label))
        
        return examples  # 返回示例列表
    
def convert_examples_to_features(args, examples, label_list, max_seq_length, tokenizer):
    label_map = {label: i for i, label in enumerate(label_list)}  # 将标签映射为索引

    features = []  # 存储特征的列表

    for (ex_index, example) in tqdm(enumerate(examples), desc="convert examples"):
        textlist = example.text.split(" ")  # 将文本分割成词语列表
        labellist = example.label.split(" ")  # 将标签序列分割成标签列表
        assert len(textlist) == len(labellist)  # 确保词语和标签序列长度一致
        tokens = []
        labels = []
        ori_tokens = []

        for i, word in enumerate(textlist):
            token = tokenizer.tokenize(word)  # 对词语进行分词
            tokens.extend(token)  # 将分词结果添加到tokens列表中
            label_1 = labellist[i]
            ori_tokens.append(word)

            # 对每个分词结果进行标签映射
            for m in range(len(token)):
                if m == 0:
                    labels.append(label_1)
                else:
                    if label_1 == "O":
                        labels.append("O")
                    else:
                        labels.append("I")

        # 如果分词后的序列长度超过最大序列长度，则进行截断
        if len(tokens) >= max_seq_length - 1:
            tokens = tokens[0:(max_seq_length - 2)]
            labels = labels[0:(max_seq_length - 2)]
            ori_tokens = ori_tokens[0:(max_seq_length - 2)]

        ori_tokens = ["[CLS]"] + ori_tokens + ["[SEP]"]

        ntokens = []
        segment_ids = []
        label_ids = []
        ntokens.append("[CLS]")
        segment_ids.append(0)
        label_ids.append(label_map["O"])

        for i, token in enumerate(tokens):
            ntokens.append(token)
            segment_ids.append(0)
            label_ids.append(label_map[labels[i]])

        ntokens.append("[SEP]")
        segment_ids.append(0)
        label_ids.append(label_map["O"])
        input_ids = list(tokenizer.convert_tokens_to_ids(ntokens))
        input_mask = [1] * len(input_ids)
        # 短的补
        lenInput = len(input_ids)
        while lenInput < max_seq_length:
            input_ids.append(0)
            segment_ids.append(0)
            input_mask.append(0)
            ntokens.append("[PAD]")
            label_ids.append(label_map["O"])
            lenInput += 1
        # 断言保证各个列表长度一致
        # assert len(ori_tokens) == len(ntokens), f"{len(ori_tokens)}, {len(ntokens)}, {ori_tokens}"
        assert len(ntokens) == max_seq_length
        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length
        assert len(label_ids) == max_seq_length

        # 如果是前5个样本，记录日志
        if ex_index < 5:
            logger.info("*** Example ***")
            logger.info("guid: %s" % (example.guid))
            logger.info("tokens: %s" % " ".join([str(x) for x in ntokens]))
            logger.info("input_ids: %s" % " ".join([str(x) for x in input_ids]))
            logger.info("input_mask: %s" % " ".join([str(x) for x in input_mask]))
            logger.info("segment_ids: %s" % " ".join([str(x) for x in segment_ids]))
            logger.info("label_ids: %s" % " ".join([str(x) for x in label_ids]))

        # 创建 InputFeatures 对象并添加到 features 列表中
        features.append(
            InputFeatures(input_ids=input_ids,
                          input_mask=input_mask,
                          segment_ids=segment_ids,
                          label_id=label_ids,
                          ori_tokens=ori_tokens))

    return features  # 返回特征列表

def get_Dataset(args, processor, tokenizer, mode="train"):
    if mode == "train":
        filepath = args.train_file
    elif mode == "eval":
        filepath = args.eval_file
    elif mode == "test":
        filepath = args.test_file
    else:
        raise ValueError("mode must be one of train, eval, or test")

    # 获取示例数据
    examples = processor.get_examples(filepath)
    label_list = args.label_list

    # 将示例数据转换为特征数据
    features = convert_examples_to_features(
        args, examples, label_list, args.max_seq_length, tokenizer
    )

    # 将特征数据转换为 PyTorch Tensor
    all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long).to(args.device)
    all_input_mask = torch.tensor([f.input_mask for f in features], dtype=torch.long).to(args.device)
    all_segment_ids = torch.tensor([f.segment_ids for f in features], dtype=torch.long).to(args.device)
    all_label_ids = torch.tensor([f.label_id for f in features], dtype=torch.long).to(args.device)

    # 创建一个 TensorDataset 对象，将数据和标签组合成一个数据集
    data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label_ids)

    # 返回示例数据、特征数据和数据集对象
    return examples, features, data