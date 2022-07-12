import os
import re
from tqdm import tqdm
from glob import glob
import json
from pprint import pprint
import argparse
from uniformize import uniformize, fill_space, 

def preprocess(lines):
    filtered_lines = []

    space_text = re.compile(' {2,}')
    bracket_text = re.compile(' *\([^)]*\)')  # (), (내용), ...
    necessary_text = re.compile('[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9.,\'\"?!@#$%^&*()\[\]{}<>/\\\-_=+\|~` ]')
    spacedot_text = re.compile('( +\.)+')
    enddot_text = re.compile('([^가-힣a-zA-Z0-9\.])\.')
    repeat_text = re.compile('([^가-힣a-zA-Z0-9\s]) *(\\1 *){3,}')
    othername_text = re.compile('name[1-9][0-9]|name[3-9]|name0')  # 제3자 이름일 확률이 높음
    username_text = re.compile(r'\bname[12]|\bname')  # 사용자 또는 상대방 이름일 확률이 상당히 높음
    
    for line in lines:
        # remove contents with square brackets
        line = line.strip()
        line = uniformize(line)
                                
        line = bracket_text.sub("", line)
        line = necessary_text.sub("", line)
        line = spacedot_text.sub("", line)
        line = enddot_text.sub("\g<1>", line)
        line = repeat_text.sub("\g<1>"*3, line)
        line = othername_text.sub("<othername>", line)  # 추후 스페셜 토큰으로 활용
        line = username_text.sub("<username>", line)  # 추후 스페셜 토큰으로 활용
        line = line.replace("account", "계정")  # 온라인 계정
        line = line.replace("socialsecuritynum", "")  # 고유 식별 번호
        line = line.replace("telnum", "")  # 전화번호
        line = line.replace("cardnum", "")  # 금융 번호
        line = line.replace("num", "")  # 기타 번호
        line = line.replace("address", "")  # 주소
        line = line.replace("affiliation", "")  # 출신, 소속
        line = line.replace("others", "")  # 기타
        line = space_text.sub(" ", line)
        
        filtered_lines.append(line.strip())
        
    return filtered_lines


data_path = "/data/nlp/모두의말뭉치/국립국어원 온라인 대화 말뭉치 2021(버전 1.0)/"

datas = glob(data_path + "*.json")

# OUTPUT PATH
output_path = "/home/nlp/preprocess/outputs/online_chat-preprocessed/"

if __name__=="__main__":
    for data in tqdm(datas):
        #print(data)
        with open(data, "r") as f:
            json_data = json.load(f)

        #pprint(json_data["document"][0])

        docs = json_data["document"]
        lines = []
        chat = ""
        speaker_id = None

        for doc in docs:
            contents = doc["utterance"]
            for content in contents:
                if content["speaker_id"] != speaker_id and chat != "":
                    lines.append(chat.strip())
                    chat = ""
                line = content["form"]
                chat += f"{line} "
                speaker_id = content["speaker_id"]
            lines.append(chat.strip() + "<|endoftext|>")
            chat = ""
        
        
        filtered_lines = preprocess(lines)

        no_chat_text = re.compile('\n *\n *\n')
        
        filtered_data = "\n".join(filtered_lines)
        filtered_data = filtered_data.replace("<|endoftext|>", "\n<|endoftext|>")  # 채팅 말뭉치에선 EOS 한 줄 띄고 사용 권장
        filtered_data = no_chat_text.sub("\n", filtered_data)

        data_name = data.split("/")[-1]
        output = output_path + data_name[:-5] + "-preprocessed.txt"

        with open(output, "w") as f:
            f.write(filtered_data)