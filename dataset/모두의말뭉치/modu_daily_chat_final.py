import os
import re
from tqdm import tqdm
from glob import glob
import json
from pprint import pprint
import argparse
from uniformize import uniformize, fill_space, pick_texts

def preprocess(lines):
    filtered_lines = []

    necessary_text = re.compile('[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9,./<>?;:\'\"\[\]{}\\\|`!@#$%^&*()\-_=+《》「」『』·ㆍ… ]')  # ~ 삭제. 데이터에 ~가 너무 많음.
    spacedot_text = re.compile('( +\.)+')
    company_text = re.compile('&companyname&\d*')
    othername_text = re.compile('name[1-9][0-9]|name[3-9]|name0')  # 제3자 이름일 확률이 높음
    username_text = re.compile(r'\bname[12]|\bname')  # 사용자 또는 상대방 이름일 확률이 상당히 높음
    address_text = re.compile('&address&\d*')
    couple_text = re.compile('\((.*)\)\/\(.*\)')  # (50만)/(오십 만), (카페에서)/(까페에서) 등 수정
    bracket_text = re.compile(' *\({1,2}([^)]*)\){1,2}')
    x_text = re.compile('x{2,}')
    

    for line in lines:
        line = fill_space(line)
        line = uniformize(line)
        line = pick_texts(line)
                                
        line = necessary_text.sub("", line)
        line = spacedot_text.sub("", line)
        line = company_text.sub("", line)
        line = othername_text.sub("<othername>", line)
        line = username_text.sub("<username>", line)
        line = address_text.sub("", line)
        line = couple_text.sub("\g<1>", line)  # 둘 중 앞의 내용으로 적용
        line = bracket_text.sub(" \g<1>", line)
        line = x_text.sub("", line)
        line = space_text.sub(" ", line)
        
        filtered_lines.append(line.strip())
        
    return filtered_lines


data_path = "/data/nlp/모두의말뭉치/국립국어원 일상 대화 말뭉치 2020(버전 1.2)/"

datas = glob(data_path + "*.json")

# OUTPUT PATH
output_path = "/home/nlp/preprocess/outputs/daily_chat-preprocessed/"

# re compile 듬는 말 지우기 위해
error_text = re.compile('\-([^\-\s]+)\-')

test = []

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
                # original form에서 더듬는 말(예시: "-하- 하려고") 찾아서 form 데이터에서 해당 부분 삭제
                check_errors = error_text.finditer(content["original_form"])  # 더듬는 부분 찾기
                for check_error in check_errors:  # 2개 이상인 경우도 존재하므로 finditer로 찾은 뒤 반복
                    error_part = check_error.group(1)  # -과 - 사이의 텍스트만 추출
                    n = line.count(error_part)  # form 데이터에서 해당 텍스트 개수 확인
                    overlap_part = f"{error_part} {error_part}"  # 검색에 도움되는 overlap 텍스트 지정
                    if n == 1:  # 1개일 경우 바로 삭제
                        line = line.replace(f"{error_part} ", "")
                    elif overlap_part in content["form"]:  # 2개 이상일 경우, "하 하려고" 처럼 동일문자 처리
                        line = re.sub(f"^{overlap_part}", error_part, line)
                        line = re.sub(f" {overlap_part}", f" {error_part}", line)
                    else:  # 2개 이상일 경우, "여 영화를" 처럼 다른 문자 처리
                        line = re.sub(f"^{error_part}\s", "", line)
                        line = re.sub(f"\s{error_part}\s", " ", line)
                        
                chat += f"{line} "
                speaker_id = content["speaker_id"]
            lines.append(chat.strip() + "<|endoftext|>")
            chat = ""
        
        filtered_lines = preprocess(lines)

        filtered_data = "\n".join(filtered_lines)
        filtered_data = filtered_data.replace("<|endoftext|>", "\n<|endoftext|>")  # 채팅 말뭉치에선 EOS 한 줄 띄고 사용 권장

        data_name = data.split("/")[-1]
        output = output_path + data_name[:-5] + "-preprocessed.txt"

        with open(output, "w") as f:
            f.write(filtered_data)