from multiprocessing import Pool
from utils import utils, common_process
from time import time
from typing import Optional
from kss import split_sentences
from tqdm import tqdm
import itertools
import re


def process(text: str) -> Optional[str]:
    """
    텍스트 전처리
    :param text: 원본 텍스트
    :return: 전처리 된 텍스트
    """
    text = common_process.uniformize(text)  # 특수문자를 일반문자로 변환
    text = common_process.filter_text(text)  # 불필요한 문자 제거
    text = re.sub(r"[\(\{\[]\s*[\)\}\]]", "", text)  # 내용없는 괄호(){}[] 삭제
    text = common_process.normalize_space(text)  # 2개 이상 공백을 1개 띄어쓰기로 정규화

    # "..." 혹은 '...', (...) 형식의 문장에서 테두리를 제거하고 ...만 남김
    if text.startswith(('"', "'", "(")) and\
            text.endswith(('"', "'", ")")):
        text = text[1:-1]

    sents = split_sentences(text)  # 문장 분리

    return sents


def main(input: str, output: str, num_process: int):
    lines = utils.load_text(input)

    result = []
    with Pool(processes=num_process) as p:
        start = time()
        _result = p.map(process, lines)  # List[List[Optional[str]]]
        for text in tqdm(list(itertools.chain.from_iterable(_result)), desc="Processing..."):  # 이중리스트 Flatten
            if common_process.filter_length(text, 4):  # 어절 개수 제한 필터링
                result.append(text)
            else:
                continue
        end = time()
        print(f"Done! ... Consume {int(end - start)} second")

    utils.save(output, "\n".join(result))


if __name__ == '__main__':
    args = utils.parse_args()
    main(**args)