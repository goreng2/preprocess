from tqdm import tqdm
from typing import List
import os
import json


def load_text(path: str) -> List[str]:
    """
    파일 불러오기
    :param path: 파일 경로
    :return: 개행 단위로 구분된 텍스트 리스트
    """
    result = []
    with open(path, "r", encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="Loading..."):
            line = line.strip()  # 개행("\n") 제거
            if line:  # 공백이 아닌 텍스트만 저장
                result.append(line)
            else:
                continue

    return result


def load_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        result = json.load(f)

    return result


def save(path: str, text: str) -> None:
    """
    파일 저장
    :param path: 파일 저장 경로
    :param text: 저장할 파일 내용
    """
    dirname = os.path.dirname(path)  # 폴더 경로 파싱
    if dirname:  # 폴더 경로가 있을 경우
        os.makedirs(dirname, exist_ok=True)  # 해당 폴더 경로 생성
    else:
        pass

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
