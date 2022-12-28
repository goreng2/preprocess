from typing import List
import re
import os
from tqdm import tqdm
import parmap


def uniformize(text: str) -> str:
    """
    특수문자를 일반문자로 변환
    :param text: 텍스트
    :return: 변환된 텍스트
    """
    # ㅁ
    text = text.replace("＃", "#")
    text = text.replace("＆", "&")
    text = text.replace("＊", "*")
    text = text.replace("＠", "@")

    # ㄴ
    text = text.replace("＂", "\"")
    text = text.replace("（", "(")
    text = text.replace("）", ")")
    text = text.replace("［", "[")
    text = text.replace("］", "]")
    text = text.replace("｛", "{")
    text = text.replace("｝", "}")
    text = text.replace("‘", "'")
    text = text.replace("’", "'")
    text = text.replace("“", "\"")
    text = text.replace("”", "\"")
    text = text.replace("〔", "[")
    text = text.replace("〕", "]")
    text = text.replace("〈", "<")
    text = text.replace("〉", ">")

    # ㄹ
    text = text.replace("％", "%")

    # ㄱ
    text = text.replace("　", " ")
    text = text.replace("！", "!")
    text = text.replace("＇", "'")
    text = text.replace("，", ",")
    text = text.replace("．", ".")
    text = text.replace("／", "/")
    text = text.replace("：", ":")
    text = text.replace("；", ";")
    text = text.replace("？", "?")
    text = text.replace("、", ",")
    text = text.replace("∼", "~")
    text = text.replace("´", "'")
    text = text.replace("～", "~")

    # ㄷ
    text = text.replace("＋", "+")
    text = text.replace("－", "-")
    text = text.replace("＜", "<")
    text = text.replace("＝", "=")
    text = text.replace("＞", ">")

    # edit special characters
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&amp;", "&")
    text = text.replace("&quot;", "\"")

    return text


def filter_text(text: str) -> str:
    """
    필요한 문자 이외의 것 제거 (영어 외 외국어 등)
    :param text: 텍스트
    :return: 불필요한 문자 제거 후 남은 텍스트
    """
    text = re.sub(r"[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9,./<>?;:\'\"\[\]{}\\\|`~!@#$%^&*()\-_=+《》「」『』·ㆍ… ]", " ", text)

    return text


def normalize_space(text: str) -> str:
    """
    여러 공백(띄어쓰기, 개행 등)을 하나의 공백(띄어쓰기)으로 치환
    :param text:
    :return:
    """
    text = re.sub(r"\s{2,}", " ", text)  # 2개 이상 공백을 1개 공백으로 정규화
    text = text.strip()

    return text


def eojeol_len_filter(lines: List[str], min_eojeol_len: int) -> List[str]:
    results = []
    for line in tqdm(lines, desc="eojeol_len_filter"):
        if len(line.split()) >= min_eojeol_len:
            results.append(line)
        else:
            continue

    return results


def remove_duplication(lines: List[str]) -> List[str]:
    print("Remove Duplication ...")
    results = list(set(lines))

    return results


class BaseProcessor:
    def __init__(self, input_path, output_path, min_word_len=4):
        self.input_path = input_path
        self.output_path = output_path
        self.min_word_len = min_word_len

    def load(self):
        lines = []
        with open(self.input_path, "r", encoding="utf-8") as f:
            for line in tqdm(f.readlines(), desc="Loading"):
                # 개행("\n") 제거
                line = line.strip()

                # 공백이 아닌 텍스트만 저장
                if line:
                    lines.append(line)
                else:
                    continue

        return lines

    def pre_process(self, line):
        line = uniformize(line)  # 특수문자를 일반문자로 변환
        line = filter_text(line)  # 불필요한 문자 제거
        line = re.sub(r"[\(\{\[]\s*[\)\}\]]", "", line)  # 내용없는 괄호(){}[] 삭제
        line = normalize_space(line)  # 2개 이상 공백을 1개 띄어쓰기로 정규화

        return line

    def post_process(self, lines):
        lines = eojeol_len_filter(lines, self.min_word_len)
        lines = remove_duplication(lines)

        return lines

    def save(self, object):
        # 저장 경로 파싱 & 생성
        dir_path = os.path.dirname(self.output_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        else:
            pass

        # 저장
        with open(self.output_path, "w", encoding="utf-8") as f:
            if isinstance(object, list):
                f.write("\n".join(object))
            else:
                f.write(object)

    def run(self):
        lines = self.load()
        lines = parmap.map(self.pre_process, lines, pm_pbar={"desc": "Process"})
        lines = self.post_process(lines)
        self.save(lines)


class Aihub전문분야Processor(BaseProcessor):
    def pre_process(self, line):
        line = uniformize(line)  # 특수문자를 일반문자로 변환
        line = filter_text(line)  # 불필요한 문자 제거

        line = line.replace("<BR>", " ")
        line = re.sub(r"&#[0-9]+;", "", line)  # ex. &#8228;, &#10061;, &#65379;
        line = normalize_space(line)  # 2개 이상 공백을 1개 띄어쓰기로 정규화

        return line


class Aihub법률규정Processor(BaseProcessor):
    pass


class PoliceProcessor(BaseProcessor):
    def pre_process(self, line):
        line = uniformize(line)  # 특수문자를 일반문자로 변환
        line = filter_text(line)  # 불필요한 문자 제거

        line = re.sub(r"&#[0-9]+;", "", line)  # ex. &#8228;, &#10061;, &#65379; 삭제
        line = re.sub(r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", " ", line)  # 이메일 삭제
        line = re.sub(r"(https?://)[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+/[a-zA-Z0-9-_/.?=&%+#]*", " ", line)  # URL 삭제
        line = normalize_space(line)  # 2개 이상 공백을 1개 띄어쓰기로 정규화
        line = re.sub(r"(,\s+){2,}", " ", line)  # ex. , , , , ,
        line = re.sub(r"(\.\s+){2,}", " ", line)  # ex. . . .
        line = re.sub(r"(\|\s+){2,}", " ", line)  # ex. | | | |
        line = re.sub(r"(=\s+){2,}", " ", line)  # ex. = = = = = = = = = = = = = = = = = =
        line = re.sub(r"(·\s+){2,}", " ", line)  # ex. · · · ·
        line = re.sub(r"(_\s+){2,}", " ", line)  # ex. _ _ _ _ _ _
        line = re.sub(r"·{2,}", " ", line)  # ex. ·····
        line = re.sub(r"(={2,}\s+){2,}", " ", line)  # ex. === ==== ==== ==== ====
        line = re.sub(r"-{2,}", " ", line)  # ex. -------------
        line = re.sub(r"…{2,}", " ", line)  # ex. ………………
        line = re.sub(r"[\(\{\[]\s*[\)\}\]]", "", line)  # 내용없는 괄호(){}[] 삭제
        line = normalize_space(line)  # 2개 이상 공백을 1개 띄어쓰기로 정규화

        return line


class Aihub2021022Processor(BaseProcessor):
    def pre_process(self, line):
        line = uniformize(line)  # 특수문자를 일반문자로 변환
        line = filter_text(line)  # 불필요한 문자 제거
        line = re.sub(r"[\(\{\[]\s*[\)\}\]]", "", line)  # 내용없는 괄호(){}[] 삭제
        line = normalize_space(line)  # 2개 이상 공백을 1개 띄어쓰기로 정규화

        if line.startswith(('"', "'", "(", "<")) and \
                line.endswith(('"', "'", ")", ">")):
            line = line[1:-1]

        return line


class Aihub2021030Processor(Aihub2021022Processor):
    pass


class NamuwikiProcessor(BaseProcessor):
    pass


class WikiProcessor(BaseProcessor):
    def pre_process(self, line):
        line = uniformize(line)  # 특수문자를 일반문자로 변환
        line = filter_text(line)  # 불필요한 문자 제거
        line = re.sub(r"(, ){2,}|\(, \)", "", line)  # 불필요한 문자 제거 후 나열된 쉼표 제거
        line = re.sub(r"[\(\{\[]\s*[\)\}\]]", "", line)  # 내용없는 괄호(){}[] 삭제
        line = normalize_space(line)  # 2개 이상 공백을 1개 띄어쓰기로 정규화

        return line


class Modu구어Processor(BaseProcessor):
    pass


class Modu문어Processor(Aihub2021022Processor):
    pass


class Modu신문Processor(Aihub2021022Processor):
    pass


if __name__ == '__main__':
    pass
