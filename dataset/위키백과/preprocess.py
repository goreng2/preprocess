import re
from kss import split_sentences
from tqdm import tqdm
import argparse
from utils import util, common_process
from pprint import pprint
import os
from multiprocessing import Pool
import itertools
from time import time
from typing import List


def process(text: str) -> List[str]:
    """
    텍스트 전처리
    :param text: 원본 텍스트
    :return: 전처리 된 텍스트
    """
    if re.search("<.+>", text):  # 헤더 필터링
        return []
    else:
        text = common_process.uniformize(text)  # 특수문자를 일반문자로 변환
        text = common_process.filter_text(text)  # 불필요한 문자 제거
        text = re.sub(r"(, ){2,}|\(, \)", "", text)  # 불필요한 문자 제거 후 나열된 쉼표 제거
        text = re.sub(r"[\(\{\[]\s*[\)\}\]]", "", text)  # 내용없는 괄호(){}[] 삭제
        text = common_process.normalize_space(text)  # 2개 이상 공백을 1개 띄어쓰기로 정규화

        return split_sentences(text)  # 문장 분리


def main(input_path: str, output_path: str, num_processor: int):
    # 설정값 검토
    assert os.path.isfile(input_path) and not os.path.isdir(output_path), "I/O 파일 경로 확인"
    assert num_processor < os.cpu_count(), f"총 CPU 개수 초과: {num_processor} > {os.cpu_count()}"
    assert num_processor < len(os.sched_getaffinity(0)), f"사용 가능한 CPU 개수 초과: {num_processor} > {len(os.sched_getaffinity(0))}"  # 윈도우에선 에러 발생: module 'os' has no attribute 'sched_getaffinity'

    # 파일 불러오기
    print(f"Load File... \"{input_path}\"")
    lines = util.load_text(input_path)
    print(f"Total {len(lines):,} lines")

    # 병렬 전처리
    print("Start Preprocess!")
    print(f"# of Processor: {num_processor}")
    result = []
    with Pool(processes=num_processor) as p:
        start = time()
        _result = p.map(process, lines)  # List[List[str]]
        for text in tqdm(list(itertools.chain.from_iterable(_result)), desc="Processing..."):  # 이중리스트 Flatten
            # 어절 개수 제한에서 필터링 된 None값 제거
            if common_process.filter_length(text, 4):
                result.append(text)
            else:
                continue
        end = time()
        print(f"Done! ... Consume {int(end - start)} second")
    print(f"Process Total {len(result):,} lines (- {len(lines) - len(result):,} lines)")

    # 전처리 결과 저장
    print(f"Save Result... \"{output_path}\"")
    util.save(output_path, "\n".join(result))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="위키백과 전처리")
    parser.add_argument("-i", "--input", type=str, required=True, help="원본 텍스트 파일 경로")
    parser.add_argument("-o", "--output", type=str, required=True, help="전처리 텍스트 파일 저장 경로")
    parser.add_argument("-n", "--num_process", type=int, required=True, help="사용할 병렬처리 CPU 코어 개수")
    args = parser.parse_args()
    pprint(vars(args))  # 설정값 확인

    main(*vars(args).values())
