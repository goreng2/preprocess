from tqdm import tqdm
from typing import List, Dict, Union
import os
import json
import argparse


def parse_args() -> Dict[str, Union[str, int]]:
    """
    실행 프로그램의 필요 인자 받기
    :return: {
        'input': str,
        'output': str,
        'num_process': int
    }
    """
    parser = argparse.ArgumentParser(description="데이터 추출/처리 인자 설정")
    parser.add_argument("-i", "--input", type=str, required=True, help="입력 파일/폴더 경로")
    parser.add_argument("-o", "--output", type=str, required=True, help="출력 파일 경로")
    # parser.add_argument("-n", "--num_process", type=int, required=True, help="병렬처리 CPU 코어 개수")
    args = parser.parse_args()

    # 설정값 확인
    for k, v in vars(args).items():
        print(f"{k}: {v}")

    # 설정값 검토
    # i, o, n = vars(args).values()
    # assert os.path.isfile(i) and not os.path.isdir(o), "input이 파일인지 확인, output이 폴더가 아닌지 확인"
    # assert n < os.cpu_count(), f"총 CPU 개수 초과: {n} > {os.cpu_count()}"

    return vars(args)


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
    try:
        with open(path, 'r', encoding='utf-8') as f:
            result = json.load(f)

    # [Debug] json.decoder.JSONDecodeError: Unexpected UTF-8 BOM
    except:
        with open(path, 'r', encoding='utf-8-sig') as f:
            result = json.load(f)

    return result


def save(path: str, text: str) -> None:
    """
    파일 저장
    :param path: 파일 저장 경로
    :param text: 저장할 파일 내용
    """
    dirname = os.path.dirname(path)  # 폴더 경로 파싱
    if dirname:  # 만들어야 할 폴더 경로가 있을 경우
        os.makedirs(dirname, exist_ok=True)  # 해당 폴더 경로 생성
    else:
        pass

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
