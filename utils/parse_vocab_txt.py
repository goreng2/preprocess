import argparse
from utils import load_json, save


def main(vocab_path, output_path):
    vocab = load_json(vocab_path)
    parsed_vocab = list(vocab["model"]["vocab"].keys())
    save(output_path, "\n".join(parsed_vocab))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="vocab.json을 vocab.txt로 변환")
    parser.add_argument("--vocab", type=str, required=True, help="json 형식의 vocab 파일 경로")
    parser.add_argument("--output", type=str, required=True, help="txt 형식의 vocab 파일 저장 경로")
    args = parser.parse_args()

    main(args.vocab, args.output)