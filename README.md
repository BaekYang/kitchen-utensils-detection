# DofbotC4

1. 준비 :
data 폴더를 만들고 그 안에 train, val, test 폴더를 형성한다.
그리고 그 밑에 image폴더를 만든다.
image폴더 안에는 png나 jpg파일, 그리고 그 파일에 대응하는 json파일을 넣는다.
이때 확장명 빼고 파일이름은 꼭 일치시킨다.

2. 얌파일 만들기 :
data.py를 돌려서 json을 yaml로 바꾼다.

3. 레이블 형성 :
data 폴더 안의 train, val, test 폴더 하위로 label 폴더를 만든다.
yolo로 읽을 txt파일들이다.

4. 학습시작
train.py 를 시작한다.

5. pt파일을 기반으로 Inference를 돌려 좌표에 대한 json파일을 얻는다.

깔아야하는거!

cuda 12.1에 맞는 Pytorch, numpy, 싸이킷런, ultralytics 등등.. gpt한테 cuda 12.1에 맞게 알려달라고 하세영! 
