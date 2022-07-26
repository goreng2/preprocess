import re
from kss import split_sentences
from tqdm import tqdm
from utils import common_process
from utils import utils
from multiprocessing import Pool
import itertools
from time import time
from typing import List, Optional


def process(text: str) -> List[Optional[str]]:
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
        sents = split_sentences(text)  # 문장 분리

        return sents


def main(input: str, output: str, num_process: int):
    # 파일 로드
    lines = utils.load_text(input)

    # 병렬 전처리
    result = []
    with Pool(processes=num_process) as p:
        start = time()
        _result = p.map(process, lines)  # List[List[Optional[str]]]
        for text in tqdm(list(itertools.chain.from_iterable(_result)), desc="Processing..."):  # 이중리스트 Flatten
            # 어절 개수 제한에서 필터링 된 None값 필터링
            if common_process.filter_length(text, 4):
                result.append(text)
            else:
                continue
        end = time()
        print(f"Done! ... Consume {int(end - start)} second")

    # 파일 저장
    utils.save(output, "\n".join(result))


if __name__ == '__main__':
    args = utils.parse_args()
    main(**args)