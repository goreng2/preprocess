import re
from typing import Optional


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
    text = re.sub(r"[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9,./<>?;:\'\"\[\]{}\\\|`~!@#$%^&*()\-_=+《》「」『』·ㆍ… ]", "", text)

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


def filter_length(text: str, min_limit: int) -> Optional[str]:
    """
    최소 어절 개수 필터링
    :param text: 원문 텍스트
    :param min_limit: 최소 어절 개수
    :return: 텍스트 혹은 None
    """
    if len(text.split()) >= min_limit:
        return text
    else:
        return None