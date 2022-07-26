INPUT_FILE="kowiki-20220701.txt"
OUTPUT_DIR="kowiki-20220701-shard2048"
OUTPUT_FILE_PREFIX="kowiki_"
SPLIT=2048

split -d -a 4 -n r/${SPLIT} ${INPUT_FILE} ${OUTPUT_DIR}/${OUTPUT_FILE_PREFIX}
# "-d": 숫자로 표현
#        ex) corpus_aa, corpus_ab, ... ⇒ corpus_00, corpus_01, ...
# "-a": 0을 넣어 숫자 개수 맞추기
#        ex) corpus_0000, corpus_0001, ...
# "-n r/N": 라운드로빈 방식으로 N개로 분할
