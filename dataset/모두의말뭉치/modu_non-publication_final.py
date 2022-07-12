import os
import re
from tqdm import tqdm
from glob import glob
from xml.etree.ElementTree import parse
from uniformize import uniformize

# DATA PATH

data_path = "/data/nlp/모두의말뭉치/국립국어원 비출판물 말뭉치(버전 1.1)/"
datas = glob(data_path + "*.sjml")

# OUTPUT PATH
output_path = "/home/nlp/preprocess/outputs/non-publication-preprocessed"

for data in tqdm(datas):
    #print(data)
    tree = parse(data)
    root = tree.getroot()

    contents = root[1]

    lines = []
    for content in contents:
        lines.append(content.text)
    lines.append("<|endoftext|>")

    #print(lines)

    filtered_lines = []

    bracket_text = re.compile(' *\([^)]*\)')  # (), (내용), ...
    korean_text = re.compile('[가-힣]')
    special_text = re.compile('[-!/\\#＃&＆*＊@＠§※☆★○●◎◇◆□■△▲▽▼→←↑↓↔〓◁◀▷▶♤♠♡♥♧♣⊙◈▣☞•]')
    end_text = re.compile('[\.!?\'"#].{0,6}$')

    for line in lines:
        # remove contents with square brackets
        if line == None:
            continue
        line = line.strip()
        line = uniformize(line)
        
        line = bracket_text.sub("", line)    
        filtered_lines.append(line)

    filtered_data = "\n".join(filtered_lines)
    filtered_data = filtered_data.replace("\n<|endoftext|>", "<|endoftext|>")

    data_name = data.split("/")[-1]
    output = output_path + data_name[:-5] + "-preprocessed.txt"

    with open(output, "w") as f:
        f.write(filtered_data)