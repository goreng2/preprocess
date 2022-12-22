from multiprocessing import Pool
from util import utils
from time import time
from typing import Optional
from util import common_process


def process(text: str) -> Optional[str]:
    """
    텍스트 전처리
    :param text: 원본 텍스트
    :return: 전처리 된 텍스트
    """
    text = common_process.uniformize(text)  # 특수문자를 일반문자로 변환
    text = common_process.filter_text(text)  # 불필요한 문자 제거
    text = common_process.normalize_space(text)  # 2개 이상 공백을 1개 띄어쓰기로 정규화
    text = common_process.filter_length(text, 4)  # 4개 이상 어절을 가진 문장만 살림; 미만 시 None

    return text


def main(input: str, output: str, num_process: int):
    # 파일 로드
    lines = utils.load_text(input)

    # 병렬처리
    with Pool(processes=num_process) as p:
        start = time()
        result = p.map(process, lines)
        end = time()
        print(f"Done! ... Consume {int(end - start)} second")
    # None값 필터링
    result = [i for i in result if i]  # 어절 개수에서 필터링 된 None값 제거

    # 파일 저장
    utils.save(output, "\n".join(result))


if __name__ == '__main__':
    args = utils.parse_args()
    main(**args)
