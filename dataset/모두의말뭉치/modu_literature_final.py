import os
import re
from tqdm import tqdm
from glob import glob
import json
from pprint import pprint
import argparse
from uniformize import uniformize

def preprocess(lines):
    filtered_lines = []

    space_text = re.compile(' {2,}')
    bracket_text = re.compile(' *\([^)]*\)')  # (), (내용), ...
    necessary_text = re.compile('[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9,./<>?;:\'\"\[\]{}\\\|`~!@#$%^&*()\-_=+《》「」『』·ㆍ… ]')
    
    for line in lines:
        # remove contents with square brackets
        line = line.strip()
        line = uniformize(line)
        
        line = necessary_text.sub("", line)
        line = bracket_text.sub("", line)
        line = space_text.sub(" ", line)
        
        filtered_lines.append(line)
        
    return filtered_lines


# DATA PATH

data_path = "/data/nlp/모두의말뭉치/국립국어원 문어 말뭉치(버전 1.0)/"
datas = glob(data_path + "*.json")

# OUTPUT PATH
output_path = "/home/nlp/preprocess/outputs/literature-preprocessed/"

if __name__=="__main__":
    for data in tqdm(datas):
        #print(data)
        with open(data, "r") as f:
            json_data = json.load(f)

        #pprint(json_data["document"][0])

        docs = json_data["document"]
        lines = []

        for doc in docs:
            contents = doc["paragraph"]
            for content in contents:
                line = content["form"]
                lines.append(line)
            lines.append("<|endoftext|>")

        filtered_lines = preprocess(lines)

        filtered_data = "\n".join(filtered_lines)
        filtered_data = filtered_data.replace("\n<|endoftext|>", "<|endoftext|>")

        data_name = data.split("/")[-1]
        output = output_path + data_name[:-5] + "-preprocessed.txt"

        with open(output, "w") as f:
            f.write(filtered_data)