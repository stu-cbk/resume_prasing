import sys
sys.path.append("D:/resume/pythonApi/NERModel")
from models import BERT_BiLSTM_CRF
import argparse
import torch
import os
from transformers import (WEIGHTS_NAME, BertConfig, BertTokenizer)
from torch.utils.data import TensorDataset
from torch.utils.data import (DataLoader, RandomSampler, SequentialSampler,
                              TensorDataset)
from tqdm import tqdm
import pickle
import os

# 获取当前脚本所在的路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 设置工作目录为当前脚本所在路径
os.chdir(current_dir)

class InputFeatures(object):
    """A single set of features of data."""
    def __init__(self, input_ids, input_mask, segment_ids,ori_tokens):
        self.input_ids = input_ids  # 输入的id
        self.input_mask = input_mask # 输入的掩码 表示有效位
        self.segment_ids = segment_ids # 段落标识符
        self.ori_tokens = ori_tokens  # 原始词语

def boolean_string(s):
    if s not in {'False', 'True'}:
        raise ValueError('Not a valid boolean string')
    return s == 'True'


def collate_fn(data:str,maxlen:int,tokenizer,device):
    datalist = list(data)
    ori_datas = []
    s = 0
    e = maxlen - 2
    while e < len(data):
        sentence = datalist[s:e]
        sentence = ['[CLS]'] + sentence + ['[SEP]']
        ori_datas.append(sentence)
        e += maxlen - 2
        s += maxlen - 2
    if e > len(data):
        sentence = datalist[s:len(data)]
        sentence = ['[CLS]'] + sentence + ['[SEP]']
        nowlen = len(sentence)
        t = [1] * nowlen
        sentence = sentence + ['[PAD]'] * (maxlen - nowlen)
        t = t + [0] * (maxlen - nowlen)
        ori_datas.append(sentence)
    features = []
    i = 0
    for sentence in ori_datas:
        input_ids = list(tokenizer.convert_tokens_to_ids(sentence))
        input_mask = []
        if i == len(ori_datas) - 1 and e > len(data):
            input_mask = t
        else:
            input_mask = [1] * len(input_ids)
        segment_ids = [0] * len(input_ids)
        features.append(
            InputFeatures(input_ids=input_ids,
                          input_mask=input_mask,
                          segment_ids=segment_ids,
                          ori_tokens=sentence))
        i += 1
    all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long).to(device)
    all_input_mask = torch.tensor([f.input_mask for f in features], dtype=torch.long).to(device)
    all_segment_ids = torch.tensor([f.segment_ids for f in features], dtype=torch.long).to(device)
    data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids)
    return features,data

def information(kind:str,data:str):

    parser = argparse.ArgumentParser()
    parser.add_argument("--max_seq_length", default=64, type=int)
    parser.add_argument("--output_dir", default="./model/bert_bilstm_crf", type=str)
    parser.add_argument("--do_lower_case", action='store_true')
    parser.add_argument("--eval_batch_size", default=16, type=int)
    parser.add_argument("--need_birnn", default=True, type=boolean_string)
    parser.add_argument("--rnn_dim", default=256, type=int)
    args = parser.parse_args()

    tokenizer = BertTokenizer.from_pretrained(args.output_dir, do_lower_case=args.do_lower_case)
    args = torch.load(os.path.join(args.output_dir, 'training_args.bin'))
    model = BERT_BiLSTM_CRF.from_pretrained(args.output_dir, need_birnn=args.need_birnn, rnn_dim=args.rnn_dim)
    
    device = torch.device("cpu")
    model.to(device)
    
    features,test_data = collate_fn(data,args.max_seq_length,tokenizer,device)
    test_sampler = SequentialSampler(test_data)
    test_dataloader = DataLoader(test_data, sampler=test_sampler, batch_size=args.eval_batch_size)
    
    if os.path.exists(os.path.join(args.output_dir, "label2id.pkl")):
        with open(os.path.join(args.output_dir, "label2id.pkl"), "rb") as f:
            label2id = pickle.load(f)
    
    id2label = {value:key for key,value in label2id.items()} 

    pred_labels = []
    all_ori_tokens = []
    for f_i in range(0,len(features)):
        f = features[f_i]
        if f_i == len(features) - 1:
            for f_j in range(1,len(f.ori_tokens)-1):
                if f.ori_tokens[f_j] == "[SEP]":
                    break
                else:
                    all_ori_tokens.append(f.ori_tokens[f_j])
        else: 
            all_ori_tokens += f.ori_tokens[1:len(f.ori_tokens)-1]

    for b_i, (input_ids, input_mask, segment_ids) in enumerate(tqdm(test_dataloader, desc="Predicting")):
        input_ids = input_ids.to(device)
        input_mask = input_mask.to(device)
        segment_ids = segment_ids.to(device)
        with torch.no_grad():
            logits = model.predict(input_ids, segment_ids, input_mask)
        for l in logits:
            pred_label = []
            for idx in l:
                pred_label.append(id2label[idx])
            pred_labels += pred_label[1:len(pred_label)-1]
    assert len(pred_labels) == len(all_ori_tokens)
    labeldict = {"职称":"TITLE","学历":"EDU","姓名":"NAME","公司":"ORG","专业":"PRO","民族":"RACE"}
    target = labeldict[kind]
    res = "UN"
    for l_i in range(0,len(pred_labels)):
        if pred_labels[l_i] == 'B-' + target:
            l_j = l_i + 1
            while l_j < len(pred_labels):
                if pred_labels[l_j] == 'I-' + target:
                    l_j += 1
                else:
                    break
            if (l_j == l_i + 1): continue
            res = ''.join(all_ori_tokens[l_i:l_j])
            break
    print(res)
    return res

# information("公司","本科")