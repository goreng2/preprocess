# PVo 사내 데이터 전처리기
데이터셋 별 전처리 소스를 통합 관리합니다.

## Requirements
```
$ pip install -r requirements.txt
```

## Usage
### 나무위키
#### 도움말
```
$ python dataset/나무위키/preprocess.py --help
```
#### 사용 예시
```
$ python dataset/나무위키/preprocess.py
    --src dataset/나무위키/namuwiki-210301-part1.txt
    --dst dataset/나무위키/result.txt
    --processor 6
```