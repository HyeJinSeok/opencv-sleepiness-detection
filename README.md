# OpenCV를 이용한 졸음 감지

<br>

이 프로젝트는 **OpenCV**와 **dlib**을 활용하여 **실시간 졸음 감지 시스템**을 구현했다. <br>

얼굴 랜드마크를 이용해 **눈 깜빡임 비율**(Eye Aspect Ratio, EAR)을 계산하고 <br>

일정 시간 이상 눈이 감겨 있으면, 졸음 상태로 판단하여 Alert를 울린다. <br>

구현 과정에서 다음의 깃허브 프로젝트를 참고하였다: 

📌 [fiyero / OpenCV_Dlib_drunk_sleepy_alert_for_driver](https://github.com/fiyero/OpenCV_Dlib_drunk_sleepy_alert_for_driver)  

📌 [akshaybahadur21 / Drowsiness_Detection](https://github.com/akshaybahadur21/Drowsiness_Detection)  

<br>

### 📆 프로젝트 기간

&nbsp; **2023.05.24 ~ 06.07**

<br>

### ⚙️사용 기술

&nbsp;- **Python 3.x**

&nbsp;- **OpenCV**: 이미지와 영상 데이터를 다루는 오픈소스 라이브러리 (얼굴 추적, 객체 감지, 영상 전처리 등) <br>

&nbsp;- **dlib**: 머신러닝과 컴퓨터비전 알고리즘을 담은 라이브러리 (얼굴 랜드마크 검출) <br>

&nbsp;- **imutils**: OpenCV 코드 작성 시 이미지 크기 조정, 회전, 좌표 변환 등을 간편하게 처리 <br>

&nbsp;- **numpy / scipy**: 벡터·행렬 연산, 거리 계산, 수학 연산을 빠르게 수행 <br>

<br>

### 🔋졸음 감지에 필요한 요소


&nbsp;• 눈이 감겼는지 인식: 눈꺼풀이 닫혔는가 열렸는가 <br>

&nbsp;• 눈이 감기면 **눈의 세로축**이 짧아지게 됨 <br>

&nbsp;• 단순한 눈 깜빡임인지 졸음인지도 구분해야 함 <br>

&nbsp;• 눈이 감겨있는 **시간 측정** 필요

<img src="images/eye.png" alt="Eye" width="200"/>

<br>

### 💡구현 방법

.py 코드 바로가기


## ① 얼굴 감지 (Face Detection)

**▪ 원리** <br>

카메라 영상 속에서 사람의 얼굴 위치를 찾는 단계에 해당함 <br>

HOG(Histogram of Oriented Gradients) + SVM(Support Vector Machine) 기반 감지기 사용 <br>

**▪ 코드** <br>

dlib이 제공하는 얼굴 감지기를 호출해 카메라 프레임 속 얼굴 영역을 탐지함 <br>

detect = dlib.get_frontal_face_detector( ) <br>

<br>

## ② 얼굴 랜드마크 검출 (Facial Landmark Detection)

**▪ 원리** <br>

감지된 얼굴에서 눈, 코, 입, 턱 등 68개의 특징점 좌표를 추출함 <br>

특히 눈 주변 좌표(6개)는 EAR 계산에 직접 사용됨 <br>

**▪ 코드** <br>

dlib이 제공하는 사전학습된 랜드마크 예측 모델을 이용해 좌표를 도출함 <br>

predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") <br>

<br>

## ③ EAR 계산 (Eye Aspect Ratio)

**▪ 원리** <br>

눈이 감겼는지 여부를 정량적으로 계산하는 지표 <br>

눈 세로 거리(A, B)와 가로 거리(C)를 이용: &nbsp;**EAR = (A + B) / (2.0 * C)** <br>

EAR 값이 작아질수록 눈이 감긴 상태 <br>

