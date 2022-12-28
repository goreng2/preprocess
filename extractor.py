import parmap
from glob import glob
import os
import json
from namuwiki.extractor import extract_text
from collections import defaultdict
import itertools


def load_json(path: str):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            result = json.load(f)

    # [Debug] json.decoder.JSONDecodeError: Unexpected UTF-8 BOM
    except:
        with open(path, 'r', encoding='utf-8-sig') as f:
            result = json.load(f)

    return result


class BaseExtractor():
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def parse_paths(self):
        root_path = os.path.join(self.input_path, "**/*.json")
        json_paths = glob(root_path, recursive=True)

        return json_paths

    def extract(self, path):
        raise Exception("해당 클래스의 extract() 메소드 오버라이딩이 필요합니다.")

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
        json_paths = self.parse_paths()
        json_texts = parmap.map(self.extract, json_paths, pm_pbar={"desc": "Extract"})
        self.save(json_texts)


class Aihub전문분야Extractor(BaseExtractor):
    def extract(self, path):
        json_body = load_json(path)

        sents = []
        for data in json_body["data"]:
            keys = data.keys()

            # 라벨 데이터 파싱
            if "rows" in keys:
                sents.append(data["title"])
                for row in data["rows"]:
                    sents.append(row["text"])

            # 원천 데이터 파싱
            elif "text" in keys:
                sents.append(data["text"])

            # 원천 데이터 파싱2
            elif "sentence" in keys:
                sents.append(data["sentence"][0]["text"])

            else:
                print("KeyError", path)
                break

        text = "\n".join(sents)

        return text


class Aihub법률규정Extractor(BaseExtractor):
    def extract(self, path):
        sents = []
        json_body = load_json(path)
        keys = json_body.keys()

        # 판결문
        if "disposal" in keys:
            for sent in json_body["disposal"]["disposalcontent"]:
                sents.append(sent)
            for sent in json_body["mentionedItems"]["rqestObjet"]:
                sents.append(sent)
            for sent in json_body["assrs"]["acusrAssrs"]:
                sents.append(sent)
            for sent in json_body["assrs"]["dedatAssrs"]:
                sents.append(sent)
            for sent in json_body["facts"]["bsisFacts"]:
                sents.append(sent)
            for sent in json_body["dcss"]["courtDcss"]:
                sents.append(sent)
            for sent in json_body["close"]["cnclsns"]:
                sents.append(sent)

        # 약관/유리
        elif "comProvision" in keys:
            for sent in json_body["clauseArticle"]:
                sents.append(sent)
            for sent in json_body["comProvision"]:
                sents.append(sent)

        # 약관/불리
        elif "illdcssBasiss" in keys:
            for sent in json_body["clauseArticle"]:
                sents.append(sent)
            for sent in json_body["illdcssBasiss"]:
                sents.append(sent)
            for sent in json_body["relateLaword"]:
                sents.append(sent)

        else:
            raise Exception(f"KeyError {path}")

        # 문장 사이사이 개행 제거
        sents = [sent.replace("\n", " ") for sent in sents]

        text = "\n".join(sents)

        return text


class Aihub2021022Extractor(BaseExtractor):
    def extract(self, path):
        json_body = load_json(path)
        sents = []
        passage = json_body["Meta(Refine)"]["passage"].split("\n")
        sents.extend(passage)

        annotation = json_body["Annotation"]
        smry1 = annotation["summary1"]
        sents.append(smry1)

        cls = path.split("/")[-2]
        if cls == "20per":
            sents.append(annotation["summary3"])
        else:  # 2~3sent
            sents.append(annotation["summary2"])

        text = "\n".join(sents)

        return text


class Aihub2021030Extractor(BaseExtractor):
    def extract(self, path):
        sents = []
        json_body = load_json(path)
        for named_entity in json_body["named_entity"]:
            for content in named_entity["content"]:
                sents.append(content["sentence"])

        text = "\n".join(sents)

        return text


class NamuwikiExtractor(BaseExtractor):
    def extract(self, path):
        return extract_text(path['text'])


class Modu구어Extractor(BaseExtractor):
    def extract(self, path):
        json_body = load_json(path)
        document = json_body["document"]
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


class Modu문어Extractor(BaseExtractor):
    def extract(self, path):
        json_body = load_json(path)

        document = json_body["document"]
        assert len(document) == 1, "Document가 복수개입니다."

        paras = document[0]["paragraph"]
        form = [para["form"] for para in paras]

        text = "\n".join(form)

        return text


class Modu신문Extractor(BaseExtractor):
    def extract(self, path):
        json_body = load_json(path)
        docs = json_body["document"]

        forms = []
        for doc in docs:
            paras = doc["paragraph"]
            for para in paras:
                form = para["form"]
                forms.append(form)

        text = "\n".join(forms)

        return text


class Modu일상Extractor(BaseExtractor):
    def extract(self, path):
        json_body = load_json(path)

        document = json_body["document"]
        assert len(document) == 1, "Document가 복수개입니다."

        utterance = document[0]["utterance"]
        form = [utter["form"] for utter in utterance]

        text = " ".join(form)

        return text


if __name__ == '__main__':
    pass
