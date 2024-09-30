import cv2
import os

# 현재 작업 중인 폴더 기준 상대경로 설정
video_folder_path = r'video'
output_folder_path = os.path.join(video_folder_path, 'videoCut')

# 저장할 폴더가 없으면 생성
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 동영상 파일 확장자 설정
video_extension = '.mp4'

# 동영상 파일들을 읽어서 처리
for video_file in os.listdir(video_folder_path):
    if video_file.endswith(video_extension):
        video_path = os.path.join(video_folder_path, video_file)
        
        # 각 동영상 파일별로 폴더 생성
        base_filename = os.path.splitext(video_file)[0]
        individual_output_folder = os.path.join(output_folder_path, base_filename)
        if not os.path.exists(individual_output_folder):
            os.makedirs(individual_output_folder)
        
        # 비디오 캡처 객체 생성
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)  # 프레임 레이트 가져오기
        
        # 프레임 번호 초기화
        frame_number = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # 프레임을 1초당 30프레임으로 맞추기
            if int(cap.get(cv2.CAP_PROP_POS_FRAMES)) % int(fps / 30) == 0:
                frame_filename = f"{base_filename}_frame_{frame_number}.jpg"
                frame_path = os.path.join(individual_output_folder, frame_filename)
                cv2.imwrite(frame_path, frame)
                frame_number += 1

        cap.release()

print("모든 동영상의 프레임이 성공적으로 저장되었습니다.")
