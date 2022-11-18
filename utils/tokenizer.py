from typing import Dict, List


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        output = [line.strip() for line in f.readlines()]

    return output


def get_vocab(path: str) -> Dict[str, int]:
    with open(path, "r", encoding="utf-8") as f:
        tokens = [line.split(maxsplit=1)[0] for line in f.readlines()]

    vocab = {}
    for index, token in enumerate(tokens):
        vocab[token.rstrip()] = index

    return vocab


def tokenize(text: str, vocab: Dict[str, int]) -> List[str]:
    total_tokens = []
    words = text.split()
    for word in words:
        start = 0
        is_unk = False
        tokens = []
        while start < len(word):
            end = len(word)
            token = None
            while start < end:
                _token = "".join(word[start:end])
                if start > 0:
                    _token = "▁" + _token
                if _token in vocab:
                    token = _token
                    break
                end -= 1

            if token is None:
                is_unk = True
                break
            tokens.append(token)
            start = end

        if is_unk:
            total_tokens.append("[UNK]")
        else:
            total_tokens.extend(tokens)

    return total_tokens


def main():
    vocab = get_vocab("../test/vocab.txt")

    result = []
    lines = load("../test/text-processed.txt")
    for line in lines:
        tokens = tokenize(line, vocab)
        result.append(" ".join(tokens))

    with open("../test/text-tokenized.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(result))


if __name__ == '__main__':
    main()
