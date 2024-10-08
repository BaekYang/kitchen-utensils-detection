# 간단설명서 (by JeongEun)

1. 준비 : data 폴더를 만들고 그 안에 train, val, test 폴더를 형성한다. 그리고 그 밑에 images폴더를 만든다.
2. images폴더 안에는 png나 jpg파일, 그리고 그 파일에 대응하는 json파일을 넣는다. 이때 확장명 빼고 파일이름은 꼭 일치시킨다.

3. 얌파일 만들기 : data.py를 돌려서 json을 yaml로 바꾼다.

4. 레이블 형성 : label.py를 돌린다. data 폴더 안의 train, val, test 폴더 하위로 label 폴더를 만든다. yolo로 읽을 txt파일들이다.

5. 학습시작 train.py 를 시작한다.
pt파일완성.

6. inference.py나 run_cal_cofi.py는 카메라를 연결했을 때 중심좌표를 보고싶을때 코드이다.
카메라가 연결되어 있다면 (현재 코드는 intel realsense2 기종 기준이다. )
run_cal_cofi.py를 실행할 수 있다.

7. 환경설정 : 
cuda 12.1을 추천한다. 컴퓨터 사양에 따라 다르지만,
Pytorch, numpy, 싸이킷런, ultralytics 등등.. 
gpt한테 질문을 통해 cuda 12.1에 맞게 설치하는것을 가장 추천한다.

8. 최소 이미지 개수 :
휴리스틱한 부분이기 때문에 확답할순 없다.
다만 한 레이블(디텍션할 물체 개수)당
train 1000장
val 200장
test 100장

은 되어야지 인식이 되었다.

8. 위 코드는 예시적인 것이며, 응용하여 다양한 식기를 인식할 수 있다.
본인의 재량껏 추가하면 된다.
https://docs.ultralytics.com/ko
읽어보면 기능을 손쉽게 추가할 수 있다.
