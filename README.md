# PVo 사내 데이터 전처리기
데이터셋 별 전처리 소스를 통합 관리합니다.

## Requirements
```
$ pip install -r requirements.txt
```

## Usage
`dataset` 하위 폴더에서 각각의 `extract.py`, `process.py` 참고
- 한국어 위키백과 `extract.sh`의 경우 Linux에서만 동작하며, 윈도우에서 테스트 시 [`ValueError: cannot find context for 'fork'`](https://github.com/attardi/wikiextractor/issues/287) 발생

### 유틸
#### train/test split
```
$ python utils/split.py
```
#### shard
```
$ bash utils/shard.sh
```

## Reference
- [NamuWiki Extractor](https://github.com/jonghwanhyeon/namu-wiki-extractor)
- 한국어 위키백과
  - [위키백과 다운로드](https://ko.wikipedia.org/wiki/%EC%9C%84%ED%82%A4%EB%B0%B1%EA%B3%BC:%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4_%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C)
  - [Wiki Extractor](https://github.com/attardi/wikiextractor)