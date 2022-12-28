from processor import *
from extractor import *
import argparse


def main(task, dataset, input, output):
    processor = {
        "aihub-special": {
            "extract": Aihub전문분야Extractor(input_path=input, output_path=output),
            "process": Aihub전문분야Processor(input_path=input, output_path=output),
        },
        "aihub-law": {
            "extract": Aihub법률규정Extractor(input_path=input, output_path=output),
            "process": Aihub법률규정Processor(input_path=input, output_path=output),
        },
        "police": {
            "extract": None,
            "process": PoliceProcessor(input_path=input, output_path=output),
        },
        "aihub-2021-022": {
            "extract": Aihub2021022Extractor(input_path=input, output_path=output),
            "process": Aihub2021022Processor(input_path=input, output_path=output),
        },
        "aihub-2021-030": {
            "extract": Aihub2021030Extractor(input_path=input, output_path=output),
            "process": Aihub2021030Processor(input_path=input, output_path=output),
        },
        "namuwiki": {
            "extract": NamuwikiExtractor(input_path=input, output_path=output),
            "process": NamuwikiProcessor(input_path=input, output_path=output),
        },
        "wiki": {
            "extract": None,
            "process": WikiProcessor(input_path=input, output_path=output),
        },
        "modu-talk": {
            "extract": Modu구어Extractor(input_path=input, output_path=output),
            "process": Modu구어Processor(input_path=input, output_path=output),
        },
        "modu-write": {
            "extract": Modu문어Extractor(input_path=input, output_path=output),
            "process": Modu문어Processor(input_path=input, output_path=output),
        },
        "modu-news": {
            "extract": Modu신문Extractor(input_path=input, output_path=output),
            "process": Modu신문Processor(input_path=input, output_path=output),
        },
        "modu-life": {
            "extract": Modu일상Extractor(input_path=input, output_path=output),
            "process": None
        },
        "sample": {
            "extract": None,
            "process": None
        },
    }

    p = processor[dataset][task]
    p.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", choices=["aihub-special", "aihub-law", "police",
                                                    "aihub-2021-022", "aihub-2021-030"])
    parser.add_argument("-t", "--task", choices=["extract", "process"])
    parser.add_argument("-i", "--input", type=str, required=True, help="path/to/dataset_root_dir_path")
    parser.add_argument("-o", "--output", type=str, required=True, help="path/to/output.txt")
    args = parser.parse_args()

    # 설정값 확인
    for k, v in vars(args).items():
        print(f"{k}: {v}")

    main(**vars(args))
