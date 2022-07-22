OUTPUT="/data/nlp/dataset_extracted"

python -m wikiextractor.WikiExtractor /data/nlp/dataset_raw/위키백과/kowiki-20220701-pages-articles.xml.bz2 \
    --output ${OUTPUT}/kowiki \
    --bytes 1G

echo "Create kowiki.txt"
mv ${OUTPUT}/kowiki/AA/wiki_00 ${OUTPUT}/kowiki.txt

echo "Remove ${OUTPUT}/kowiki directory"
rm -rf ${OUTPUT}/kowiki
