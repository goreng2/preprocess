from tokenizers import Tokenizer
from tokenizers import normalizers
from tokenizers.models import WordPiece
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.processors import TemplateProcessing
from tokenizers.trainers import WordPieceTrainer
from tokenizers.normalizers import Lowercase, StripAccents
import argparse


def main(corpus, size, output):
    tokenizer = Tokenizer(WordPiece(unk_token="[UNK]"))
    tokenizer.normalizer = normalizers.Sequence([Lowercase(), StripAccents()])
    tokenizer.pre_tokenizer = Whitespace()
    tokenizer.post_processor = TemplateProcessing(
        single="[CLS] $A [SEP]",
        pair="[CLS] $A [SEP] $B:1 [SEP]:1",
        special_tokens=[
            ("[CLS]", 1),
            ("[SEP]", 2),
        ],
    )

    trainer = WordPieceTrainer(
        vocab_size=size, special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"]
    )
    tokenizer.train(corpus, trainer)
    tokenizer.save(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="WordPiece Tokenizer 만들기")
    parser.add_argument("--corpus", nargs="+", type=str, required=True, help="path/to/corpus.txt")
    parser.add_argument("--size", type=int, required=True, help="Vocab 사이즈")
    parser.add_argument("--output", type=str, default="vocab.json", help="path/to/vocab.json")
    args = parser.parse_args()

    main(**vars(args))