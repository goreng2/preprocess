# PVo 사내 데이터 전처리 소스
데이터셋 별 전처리 소스를 통합 관리합니다.

## To Do
- [ ] [processor.py](processor.py)에 문장분리(KSS=1.3.1) 적용해야함

## Requirements
```
$ pip install -r requirements.txt
```

## Usage
```commandline
python main.py -h
```
- `한국어 위키백과` 데이터셋 추출의 경우 [extract_wiki.sh](extract_wiki.sh)를 사용합니다.
  - Linux에서만 동작하며, 윈도우에서 테스트 시 [`ValueError: cannot find context for 'fork'`](https://github.com/attardi/wikiextractor/issues/287)에러가 발생합니다.

### 전처리 외 유틸 사용법
#### Tokenizer (Vocab) 만들기
```commandline
python util/WPM.py -h
```

### Train / Test Split
```commandline
python util/split.py -h
```

#### 샤딩 (2048개)
```commandline
bash util/shard.sh path/to/corpus.txt
```

## Reference
- [NamuWiki Extractor](https://github.com/jonghwanhyeon/namu-wiki-extractor)
- 한국어 위키백과
  - [위키백과 다운로드](https://ko.wikipedia.org/wiki/%EC%9C%84%ED%82%A4%EB%B0%B1%EA%B3%BC:%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4_%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C)
  - [Wiki Extractor](https://github.com/attardi/wikiextractor)
