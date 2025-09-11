import cv2
import dlib
import time
import numpy as np
from scipy.spatial import distance
from imutils import face_utils

# 1. EAR 계산 함수 정의

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])  # 세로 거리 1
    B = distance.euclidean(eye[2], eye[4])  # 세로 거리 2
    C = distance.euclidean(eye[0], eye[3])  # 가로 거리
    ear = (A + B) / (2.0 * C)
    return ear

# 2. 상수 정의

thresh = 0.25         # EAR 임계값 (이 값보다 작으면 눈 감음으로 간주)
frame_check = 20      # 연속 프레임 수 기준치
flag = 0              # 눈 감은 프레임 수 카운터

# 3. dlib 얼굴 감지기 + 랜드마크 예측 모델 로드

print("[INFO] dlib 얼굴 감지기와 랜드마크 예측 모델 로딩 중...")
detect = dlib.get_frontal_face_detector()  # 얼굴 감지기
predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")  # 랜드마크 예측 모델

# 눈의 랜드마크 인덱스 (68개 중 눈 영역: 왼쪽, 오른쪽)
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

# 4. 비디오 입력 (웹캠 사용)

cap = cv2.VideoCapture(0)  # 0 = 기본 웹캠
time.sleep(1.0)

# 5. 메인 루프

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 영상 크기 조정 및 그레이스케일 변환
    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 얼굴 탐지
    subjects = detect(gray, 0)

    for subject in subjects:
        # 얼굴 랜드마크 추출
        shape = predict(gray, subject)
        shape = face_utils.shape_to_np(shape)  # numpy array로 변환

        # 왼쪽/오른쪽 눈 좌표 추출
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        # EAR 계산
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        # 눈 윤곽선을 그려 시각화
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        # EAR 값 표시
        cv2.putText(frame, f"EAR: {ear:.2f}", (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # 6. 졸음 감지 로직

        if ear < thresh:  
            flag += 1
            # 일정 프레임 이상 눈을 감으면 경고
            if flag >= frame_check:
                cv2.putText(frame, "****************ALERT!****************",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 0, 255), 2)
                cv2.putText(frame, "****************ALERT!****************",
                            (10, 325), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 0, 255), 2)
        else:
            flag = 0  # 눈을 떴으면 카운터 초기화

    # 영상 출력
    cv2.imshow("Frame", frame)

    # ESC(27) 키로 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 7. 리소스 해제

cap.release()
cv2.destroyAllWindows()