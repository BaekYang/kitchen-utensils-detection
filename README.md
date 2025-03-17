Depth Camera로 손목 및 손 좌표 추출 및 CSV 저장

프로젝트 개요
이 프로젝트는 **Depth Camera(ZED)**를 사용하여 촬영한 영상에서 YOLOv8-Pose와 Mediapipe Hands를 활용하여 사람의 손목과 손을 인식한 후, 해당 좌표를 3D XYZ 형식으로 CSV 파일에 저장하는 코드입니다.

주요 기능
YOLOv8-Pose를 사용하여 손목(wrist) 좌표 검출
Mediapipe Hands를 사용하여 손의 중심 좌표 검출
ZED Depth Camera를 활용하여 손목 및 손의 3D 좌표 추출
결과를 CSV 파일에 저장


폴더 구조
📁 프로젝트 폴더
├── 📁 data                 # SVO 파일 저장 폴더
│   ├── example.svo        # Depth Camera에서 촬영한 SVO 파일
├── 📄 main.py              # 실행 파일 (YOLO + Mediapipe Hands 적용 코드)
├── 📄 output.csv           # 손목과 손의 3D 좌표가 저장되는 CSV 파일
├── 📄 README.md            # 프로젝트 설명서 (현재 문서)

실행 방법
1. 필요한 파일 준비
data 폴더를 만들고 SVO 파일(.svo2)을 추가합니다.
(예시: data/example.svo)

2. 필요한 라이브러리 설치
아래 명령어를 실행하여 필요한 Python 패키지를 설치합니다.
pip install ultralytics opencv-python numpy mediapipe pyzed

3. 코드 실행
터미널에서 프로젝트 폴더로 이동한 후, 다음 명령어를 입력하여 실행합니다.
python main.py --input_svo_file data/example.svo --fps 30 --visualize

4. CSV 파일 확인
코드가 실행되면 output.csv 파일이 생성되며, 손목과 손의 XYZ 좌표가 저장됩니다.
timestamp,x,y,z,label
1710765534.123,123.456,78.910,50.321,wrist
1710765534.123,125.789,80.112,52.543,hand

코드 수정 방법
코드 내에서 CSV 저장 경로를 변경하려면 main.py의 다음 부분을 수정하세요:
output_path = "output.csv"  # 기본 저장 경로
또는 실행할 때 CSV 경로를 직접 지정할 수 있습니다.
python main.py --input_svo_file data/example.svo --fps 30 --visualize --output_path my_output.csv


