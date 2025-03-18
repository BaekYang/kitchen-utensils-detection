import numpy as np

# ===========================
# 1. 대응점 데이터 입력
# ===========================
# 주어진 카메라 좌표 (독립 변수)
def set_points():
    camera_points = np.array([
        [-58, 335, 1575.5],    # 1
        [-58, 185, 1575.9],    # 2
        [-61, 341, 1376],      #3
        [-59, 191, 1377],      #4
        [  78, 342, 1375],     #5
        [  80, 190, 1355],     #6
        [  81, 334, 1560],     #7
        [  82, 185, 1565],     #8
        [-65, 279, 1656],      #9
        [-365,479,1656],       #10
        [-32, 283, 1619],      #11
        [82,141,1471],         #12
        [130, 127, 1521],      #13
        [101,213,1450],        #14
        [-38,303,1498]         #15
    ], dtype=np.float64)

    # 주어진 로봇(월드) 좌표 (종속 변수)
    robot_points = np.array([
        [100, 210, 150],    #1
        [100, 210, 300],    #2
        [300, 210, 150],    #3
        [300, 210, 300],    #4
        [300, 350, 150],    #5
        [300, 350, 300],    #6
        [100, 350, 150],    #7
        [100, 350, 300],    #8
        [0,   200, 200],    #9
        [0,   0,   0],      #10
        [50, 300, 200],     #11
        [200, 350, 350],    #12
        [130,400,360],      #13
        [230,370,280],      #14
        [170,230,185]       #15
    ], dtype=np.float64)
    return camera_points, robot_points

# ===========================
# 2. 아핀 변환 행렬 T (3x4) 계산
# ===========================
# 각 카메라 좌표에 상수 1을 추가하여 (10x4) 행렬 X 구성
def calculate_T(camera_points, robot_points):
    ones = np.ones((camera_points.shape[0], 1))
    X = np.hstack([camera_points, ones])  # shape: (10,4)

    # 최소제곱법으로 X * T^T ≈ robot_points  (즉, T^T = X^+ * robot_points)
    T_transpose, residuals, rank, s = np.linalg.lstsq(X, robot_points, rcond=None)
    T = T_transpose.T  # T: 3x4 행렬

    #print("=== Computed Affine Transform (T) ===")
    #print(T)
    return T

# ===========================
# 3. 카메라 좌표 -> 로봇 좌표 변환 함수
# ===========================


def transform_camera_to_robot(cam_coord, T):
    """
    cam_coord: (x, y, z) 카메라 좌표 (mm)
    T: 3x4 아핀 변환 행렬 (로봇 좌표 = T * [cam_coord; 1])
    반환: 로봇 좌표 (x, y, z) as 1D numpy array
    """
    p_cam = np.array([cam_coord[0], cam_coord[1], cam_coord[2], 1.0]).reshape(4, 1)
    p_robot = T @ p_cam
    return p_robot.flatten()

# ===========================
# 4. 사용자 입력 및 변환 결과 출력
# ===========================rm
if __name__ == "__main__":
    inp = input("카메라 좌표 (x,y,z, mm)를 쉼표로 입력하세요 (예: 100,210,150): ")
    try:
        vals = [float(x.strip()) for x in inp.split(',')]
        if len(vals) != 3:
            raise ValueError("세 개의 숫자를 입력해야 합니다.")
    except Exception as e:
        print("입력 오류:", e)
        import sys
        sys.exit(1)

    robot_coord = transform_camera_to_robot(vals)
    print("\n=== Transformation Result ===")
    print(f"입력된 카메라 좌표: {vals}")
    print(f"변환된 로봇(월드) 좌표: {robot_coord}")
