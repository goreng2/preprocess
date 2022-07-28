from multiprocessing import Pool
from utils import utils
from glob import glob
import os
from collections import defaultdict
import itertools


def extract(file_path: str) -> str:
    """
    json 파일에서 텍스트만을 추출합니다.
    분리된 텍스트를 화자 별로 조립 후 문장으로 만듭니다.
    :param file_path: json 파일 경로
    :return: 화자 별 문장 (line by line)
    """
    contents = utils.load_json(file_path)
    document = contents["document"]
    assert len(document) == 1, "Document가 복수개입니다."
    utters = document[0]["utterance"]

    speaker2forms = defaultdict(list)
    forms = []
    for idx, utter in enumerate(utters):
        form = utter["form"]
        if idx == 0:
            forms.append(form)
        else:
            prior_speaker = utters[idx - 1]["speaker_id"]
            now_speaker = utter["speaker_id"]
            if prior_speaker == now_speaker:
                forms.append(form)
            else:
                sent = " ".join(forms)
                speaker2forms[prior_speaker].append(sent)
                forms.clear()
                forms.append(form)

    forms_list = speaker2forms.values()
    flatten_forms_list = list(itertools.chain.from_iterable(forms_list))
    text = "\n".join(flatten_forms_list)

    return text


def main(input: str, output: str, num_process: int):
    # 파일 경로 수집
    files = glob(os.path.join(input, "*.json"))

    # 병렬처리
    with Pool(processes=num_process) as p:
        result = p.map(extract, files)

    # 결과 저장
    utils.save(output, "\n".join(result))


if __name__ == '__main__':
    args = utils.parse_args()
    main(**args)
