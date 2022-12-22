from multiprocessing import Pool
from util import utils
from time import time
from typing import Dict, Any
from namuwiki.extractor import extract_text


def extract(document: Dict[str, Any]) -> str:
    """
    오픈소스를 활용한 본문 텍스트 추출
    :param document: 나무위키 문서
    :return: 추출된 본문 텍스트
    """
    return extract_text(document['text'])


def main(input: str, output: str, num_process: int):
    # 파일 로드
    docs = utils.load_json(input)  # List[Dict[str, Any]]

    # 병렬처리
    with Pool(processes=num_process) as p:
        start = time()
        contents = p.map(extract, docs)
        end = time()
        print(f"Done! ... Consume {int(end - start)} second")

    # 파일 저장
    utils.save(output, "\n".join(contents))


if __name__ == '__main__':
    args = utils.parse_args()
    main(**args)
