import os
from multiprocessing import Pool
from namuwiki.extractor import extract_text
from utils import util
import argparse
from time import time
from typing import Dict, Any
from pprint import pprint


def extract(document: Dict[str, Any]) -> str:
    """
    오픈소스를 활용한 본문 텍스트 추출
    :param document: 나무위키 문서
    :return: 추출된 본문 텍스트
    """
    return extract_text(document['text'])


def main(input_path: str, output_path: str, num_processor: int):
    # 설정값 검토
    assert os.path.isfile(input_path) and not os.path.isdir(output_path), "I/O 파일 경로 확인"
    assert num_processor < os.cpu_count(), f"총 CPU 개수 초과: {num_processor} > {os.cpu_count()}"
    assert num_processor < len(os.sched_getaffinity(0)), f"사용 가능한 CPU 개수 초과: {num_processor} > {len(os.sched_getaffinity(0))}"  # 윈도우에선 에러 발생: module 'os' has no attribute 'sched_getaffinity'

    # 파일 로드
    print(f"Load File... \"{input_path}\"")
    docs = util.load_json(input_path)  # List[Dict]
    print(f"Total {len(docs):,} Documents")

    # 병렬처리
    print("Start Extract!")
    print(f"# of Processor: {num_processor}")
    with Pool(processes=num_processor) as p:
        start = time()
        contents = p.map(extract, docs)
        end = time()
        print(f"Done! ... Consume {int(end - start)} second")
    print(f"Total {len(contents):,} lines (- {len(docs) - len(contents):,} lines)")

    # 파일 저장
    print(f"Save Result... \"{output_path}\"")
    util.save(output_path, "\n".join(contents))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="나무위키 본문 추출")
    parser.add_argument("-i", "--input", type=str, required=True, help="원본 경로")
    parser.add_argument("-o", "--output", type=str, required=True, help="추출된 텍스트 파일 저장 경로")
    parser.add_argument("-n", "--num_process", type=int, required=True, help="사용할 병렬처리 CPU 코어 개수")
    args = parser.parse_args()
    pprint(vars(args))  # 설정값 확인

    main(*vars(args).values())
