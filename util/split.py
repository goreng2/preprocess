import os
import utils
from sklearn.model_selection import train_test_split
import argparse


def main(input: str, percent: float):
    # 결과 저장 폴더 생성
    file = os.path.basename(input)
    name, ext = file.split(".")
    split_dir = os.path.join(os.path.dirname(input), f"{name}-train{1-percent}-test{percent}")

    # Split
    lines = utils.load_text(input)
    train, test = train_test_split(lines, test_size=percent, random_state=42, shuffle=True)

    # 결과 저장
    train_path = os.path.join(split_dir, f"{name}-train.{ext}")
    test_path = os.path.join(split_dir, f"{name}-test.{ext}")
    utils.save(train_path, "\n".join(train))
    utils.save(test_path, "\n".join(test))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="train/test split")
    parser.add_argument("-i", "--input", type=str, required=True, help="path/to/corpus.txt")
    parser.add_argument("-p", "--percent", type=float, default=0.1, help="test-set percentage (0~1)")
    args = parser.parse_args()

    main(**vars(args))