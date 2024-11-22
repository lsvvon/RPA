import tensorflow as tf
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras import layers

# 문자 집합 정의
characters = ['2', '3', '4', '5', '6', '7', '8', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'k', 'm', 'n', 'p', 'q', 'r', 'v', 'w', 'x', 'y']

# 문자-숫자 변환 매핑 설정
char_to_num = layers.StringLookup(
    vocabulary=list(characters), mask_token=None
)

num_to_char = layers.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), mask_token=None, invert=True
)

# 모델 불러오기
model = load_model('./model/model_save_test_1')

# 예측을 위한 이미지 전처리
def preprocess_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # 흑백 이미지로 로드
    img = cv2.resize(img, (250, 50))  # 모델이 요구하는 크기로 리사이즈
    img = img.astype(np.float32) / 255.0  # 이미지 정규화 [0, 1] 범위
    img = img[..., np.newaxis]  # 채널 차원 추가 (250, 50, 1)
    img = img[np.newaxis, ...]  # 배치 차원 추가 (1, 250, 50, 1)
    img = tf.transpose(img, perm=[0, 2, 1, 3])  # (1, 50, 250, 1) -> (1, 250, 50, 1)
    return img

# 예측 함수
def decode_batch_predictions(pred):
    pred_texts = []
    for p in pred:
        # 가장 높은 확률의 인덱스 선택
        pred_text = tf.argmax(p, axis=-1).numpy()

        # 빈 공간(0)을 무시하고 중복된 문자 제거
        decoded_indices = []
        prev_idx = None
        for idx in pred_text:
            if idx != prev_idx:  # 중복 제거
                if idx != 0:  # 0 (blank) 제거
                    decoded_indices.append(idx)
                prev_idx = idx

        # 인덱스를 문자로 변환
        decoded_text = ''.join(
            [num_to_char(i).numpy().decode("utf-8") for i in decoded_indices]
        )

        pred_texts.append(decoded_text)
    return pred_texts

# 예측하기 위한 이미지 경로
img_path = 'C:/python/RPA/sw/capImg.png'

# 이미지 전처리
img = preprocess_image(img_path)

# 예측 수행
preds = model.predict(img)

# 예측 결과 디코딩
decoded_preds = decode_batch_predictions(preds)

# 예측 라벨 출력
print(f"Predicted label: {decoded_preds[0]}")