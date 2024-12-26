import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

# Mediapipe 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# MobileNetV2 모델 로드
model = MobileNetV2(weights="imagenet")

# 사용자 태그 설정
user_tags = ["T-shirt", "Jacket"]

# 카메라 열기
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("카메라에서 영상을 가져올 수 없습니다.")
        break

    # Mediapipe로 신체 감지
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    # 신체 영역 추출
    if results.pose_landmarks:
        for landmark in results.pose_landmarks.landmark:
            x = int(landmark.x * frame.shape[1])
            y = int(landmark.y * frame.shape[0])
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

        # 신체 바운딩 박스 추출
        x_min = int(min([lm.x for lm in results.pose_landmarks.landmark]) * frame.shape[1])
        x_max = int(max([lm.x for lm in results.pose_landmarks.landmark]) * frame.shape[1])
        y_min = int(min([lm.y for lm in results.pose_landmarks.landmark]) * frame.shape[0])
        y_max = int(max([lm.y for lm in results.pose_landmarks.landmark]) * frame.shape[0])

        body_crop = frame[y_min:y_max, x_min:x_max]
        if body_crop.size > 0:
            # MobileNetV2로 분류
            img = cv2.resize(body_crop, (224, 224))
            img = preprocess_input(img)
            img = np.expand_dims(img, axis=0)
            preds = model.predict(img)
            decoded = decode_predictions(preds, top=3)[0]
            predicted_tags = [tag for (_, tag, _) in decoded]

            # 유사도 계산
            matching_tags = set(user_tags).intersection(predicted_tags)
            similarity = len(matching_tags) / len(user_tags) * 100

            # 태그 및 유사도 표시
            for i, (tag, prob) in enumerate(decoded):
                cv2.putText(frame, f"{tag}: {prob:.2f}", (10, 30 + i * 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(frame, f"Similarity: {similarity:.2f}%", (10, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Real-Time Mediapipe Detection", frame)

    # ESC 키로 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()