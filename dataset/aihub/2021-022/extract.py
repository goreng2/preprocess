from multiprocessing import Pool
from utils import utils
from glob import glob
import os


def extract(file_path: str) -> str:
    """
    json 파일에서 텍스트만을 추출합니다.
    :param file_path: json 파일 경로
    :return: 한 줄 텍스트
    """
    sentences = []
    json = utils.load_json(file_path)
    # for named_entity in json["named_entity"]:
    #     for content in named_entity["content"]:
    #         sentences.append(content["sentence"])
    passage = json["Meta(Refine)"]["passage"].split("\n")
    sentences.extend(passage)

    annotation = json["Annotation"]
    smry1 = annotation["summary1"]
    sentences.append(smry1)

    # cls = file_path.split("\\")[-2]
    cls = file_path.split("/")[-2]
    if cls == "20per":
        sentences.append(annotation["summary3"])
    else:  # 2~3sent
        sentences.append(annotation["summary2"])

    text = "\n".join(sentences)

    return text


def main(input: str, output: str, num_process: int):
    # 파일 경로 수집
    files = glob(os.path.join(input, "01.데이터/**/라벨링데이터/**/**/*.json"))
    # files = glob(os.path.join(input, "**/*.json"))

    # 병렬처리
    with Pool(processes=num_process) as p:
        result = p.map(extract, files)

    # 결과 저장
    utils.save(output, "\n".join(result))


if __name__ == '__main__':
    """
    -i /data/nlp/dataset_raw/AIHub/개방데이터/022.요약문 및 레포트 생성 데이터
    """
    args = utils.parse_args()
    main(**args)