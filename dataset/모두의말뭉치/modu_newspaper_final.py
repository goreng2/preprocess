import os
import re
from tqdm import tqdm
from glob import glob
import json
from pprint import pprint
import argparse
from uniformize import uniformize

parser = argparse.ArgumentParser(description='모두의 말뭉치 신문 데이터 전처리기')

parser.add_argument('--data',
                    type=str,
                    choices=['1819', '2020', '2021'],
                    help='데이터를 선택해주세요. 예시) 1819, 2020, 2021')

args = parser.parse_args()

def preprocess(lines):
    filtered_lines = []

    space_text = re.compile(' {2,}')
    bracket_text = re.compile(' *\([^)]*\)')  # (), (내용), ...
    korean_text = re.compile('[가-힣]')
    special_text = re.compile('[-!/\\#＃&＆*＊@＠§※☆★○●◎◇◆□■△▲▽▼→←↑↓↔〓◁◀▷▶♤♠♡♥♧♣⊙◈▣☞•]')
    end_text = re.compile('[\.!?\'"#].{0,6}$')

    for line in tqdm(lines):
        # remove contents with square brackets
        line = line.strip()
        line = uniformize(line)
        
        line = bracket_text.sub("", line)
        line = space_text.sub(" ", line)
        
        filtered_lines.append(line)
        
    return filtered_lines


# DATA PATH

if args.data == '1819':
    data_path = "/data/nlp/모두의말뭉치/국립국어원 신문 말뭉치(버전 2.0)/"    
if args.data == '2020':
    data_path = "/data/nlp/모두의말뭉치/국립국어원 신문 말뭉치 2020(버전 1.1)/"
if args.data == '2021':
    data_path = "/data/nlp/모두의말뭉치/국립국어원 신문 말뭉치 2021(버전 1.0)/"

datas = glob(data_path + "*.json")

# OUTPUT PATH
output_path = "/home/nlp/preprocess/outputs/"

if __name__=="__main__":
    for data in datas:
        print(data)
        with open(data, "r") as f:
            json_data = json.load(f)

        #pprint(json_data["document"][0])

        docs = json_data["document"]
        lines = []

        for doc in tqdm(docs):
            contents = doc["paragraph"]
            for content in contents:
                line = content["form"]
                lines.append(line)
            lines.append("<|endoftext|>")

        #filtered_lines = preprocess(lines)

        filtered_data = "\n".join(lines)
        filtered_data = filtered_data.replace("\n<|endoftext|>", "<|endoftext|>")

        data_name = data.split("/")[-1]
        output = output_path + data_name[:-5] + "-preprocessed2.txt"

        with open(output, "w") as f:
            f.write(filtered_data)