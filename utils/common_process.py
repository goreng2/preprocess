import re

class Preprocessor:
    def __init__(self):
        self.space = re.compile(' {2,}')
        self.normal_text = re.compile('[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9,./<>?;:\'\"\[\]{}\\\|`~!@#$%^&*()\-_=+《》「」『』·ㆍ… ]')

    def uniformize(self, line):
        # change the special characters to normal charcters

        # ㅁ
        line = line.replace("＃", "#")
        line = line.replace("＆", "&")
        line = line.replace("＊", "*")
        line = line.replace("＠", "@")

        # ㄴ
        line = line.replace("＂", "\"")
        line = line.replace("（", "(")
        line = line.replace("）", ")")
        line = line.replace("［", "[")
        line = line.replace("］", "]")
        line = line.replace("｛", "{")
        line = line.replace("｝", "}")
        line = line.replace("‘", "'")
        line = line.replace("’", "'")
        line = line.replace("“", "\"")
        line = line.replace("”", "\"")
        line = line.replace("〔", "[")
        line = line.replace("〕", "]")
        line = line.replace("〈", "<")
        line = line.replace("〉", ">")

        # ㄹ
        line = line.replace("％", "%")

        # ㄱ
        line = line.replace("　", " ")
        line = line.replace("！", "!")
        line = line.replace("＇", "'")
        line = line.replace("，", ",")
        line = line.replace("．", ".")
        line = line.replace("／", "/")
        line = line.replace("：", ":")
        line = line.replace("；", ";")
        line = line.replace("？", "?")
        line = line.replace("、", ",")
        line = line.replace("∼", "~")
        line = line.replace("´", "'")
        line = line.replace("～", "~")

        # ㄷ
        line = line.replace("＋", "+")
        line = line.replace("－", "-")
        line = line.replace("＜", "<")
        line = line.replace("＝", "=")
        line = line.replace("＞", ">")

        # edit special characters
        line = line.replace("&lt;", "<")
        line = line.replace("&gt;", ">")
        line = line.replace("&amp;", "&")
        line = line.replace("&quot;", "\"")

        return line

    def fill_space(self, line):
        line = line.strip()
        # prevent more than 2 spaces
        line = self.space.sub(" ", line)

        return line

    def pick_texts(self, line, not_used_text=None):
        
