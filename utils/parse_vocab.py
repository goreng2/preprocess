import argparse
from utils import load_json, save


def main(vocab_path, output_path):
    vocab = load_json(vocab_path)
    parsed_vocab = list(vocab["model"]["vocab"].keys())
    parsed_vocab = [token.replace("##", "▁") for token in parsed_vocab]
    save(output_path, "\n".join(parsed_vocab))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="json에서 vocab 부분만 추출")
    parser.add_argument("--vocab", type=str, required=True, help="path/to/vocab.json")
    parser.add_argument("--output", type=str, required=True, help="path/to/vocab.txt")
    args = parser.parse_args()

    main(args.vocab, args.output)