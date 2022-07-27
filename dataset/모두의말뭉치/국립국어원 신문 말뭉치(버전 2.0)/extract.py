from multiprocessing import Pool
from glob import glob
from utils import utils
import os


def extract(file_path: str) -> str:
    """
    json 파일에서 텍스트만을 추출합니다.
    :param file_path: json 파일 경로
    :return: 한 줄 텍스트
    """
    contents = utils.load_json(file_path)
    docs = contents["document"]

    forms = []
    for doc in docs:
        paras = doc["paragraph"]
        for para in paras:
            form = para["form"]
            forms.append(form)

    text = "\n".join(forms)

    return text


def main(input: str, output: str, num_process: int):
    # 파일 경로 수집
    files = glob(os.path.join(input, "*.json"))

    # 병렬처리
    with Pool(processes=num_process) as p:
        result = p.map(extract, files)

    # 결과 저장
    utils.save(output, "\n".join(result))


if __name__ == "__main__":
    args = utils.parse_args()
    main(**args)
