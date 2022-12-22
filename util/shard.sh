#!/bin/bash

CORPUS="corpus-20220915-pjw1210"
CORPUS_PATH="/home/nlp/data/dataset_preprocessed/${CORPUS}-train0.9-test0.1"
NUM=2048

echo "Create train/test directory"
mkdir ${CORPUS_PATH}/train
mkdir ${CORPUS_PATH}/test

echo "Shard train/test data"
split -d -a 4 -n r/${NUM} ${CORPUS_PATH}/${CORPUS}-train.txt ${CORPUS_PATH}/train/${CORPUS}_
split -d -a 4 -n r/${NUM} ${CORPUS_PATH}/${CORPUS}-test.txt ${CORPUS_PATH}/test/${CORPUS}_
# "-d": 숫자로 표현
#        ex) corpus_aa, corpus_ab, ... ⇒ corpus_00, corpus_01, ...
# "-a": 0을 넣어 숫자 개수 맞추기
#        ex) corpus_0000, corpus_0001, ...
# "-n r/N": 라운드로빈 방식으로 N개로 분할

