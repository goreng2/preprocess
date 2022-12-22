from multiprocessing import Pool
import parmap
from util import utils
from glob import glob
import os


def extract(file_path: str) -> str:
    """
    json 파일에서 텍스트만을 추출합니다.
    :param file_path: json 파일 경로
    :return: 텍스트
    """
    sentences = []
    json = utils.load_json(file_path)
    for data in json["data"]:
        keys = data.keys()

        # 라벨 데이터 파싱
        if "rows" in keys:
            sentences.append(data["title"])
            for content in data["rows"]:
                sentences.append(content["text"])

        # 원천 데이터 파싱
        elif "text" in keys:
            sentences.append(data["text"])

        # 원천 데이터 파싱2
        elif "sentence" in keys:
            sentences.append(data["sentence"][0]["text"])

        else:
            print("KeyError", file_path)
            break

    text = "\n".join(sentences)

    return text


def main(input: str, output: str):
    # 파일 경로 수집
    files = glob(os.path.join(input, "**/*.json"), recursive=True)
    # print(files)

    # 병렬처리
    # with Pool(processes=num_process) as p:
    #     result = p.map(extract, files)
    result = parmap.map(extract, files, pm_pbar={"desc": "Extracting"})

    # 결과 저장
    utils.save(output, "\n".join(result))


if __name__ == '__main__':
    """
    -i /data/nlp/dataset_raw/AIHub/개방데이터/2020/전문분야 말뭉치
    """
    args = utils.parse_args()
    main(**args)
