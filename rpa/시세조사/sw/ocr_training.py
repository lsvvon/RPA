import os
import keras.backend
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import tensorflow as tf
import keras
from tensorflow.python.framework import ops
from keras import layers
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Path to the data directory
data_dir = Path("C:/python/RPA/캡챠")

# Get list of all the images
images = sorted(list(map(str, list(data_dir.glob("*.png")))))
labels = [img.split(os.path.sep)[-1].split(".png")[0] for img in images]
characters = set(char for label in labels for char in label)
characters = sorted(list(characters))
print('characters: ', characters)

# 배치 사이즈 지정
batch_size = 16

# image shape 지정
img_width = 200
img_height = 50

# 이미지가 convolutional blocks에 의해 downsample되는 비율을 2로 설정할 것입니다.
# 우리는 2번의 convolutional blocks를 사용할 것이기 때문에
# 이미지는 한 변을 기준으로 4배 줄어듭니다.
downsample_factor = 4

# 라벨 중 가장 긴 라벨의 길이
# max_length = max([len(label) for label in labels])
max_length = 5

# Number of images found:  500
# Number of labels found:  500
# Number of unique characters:  25
# Characters present:  ['2', '3', '4', '5', '6', '7', '8', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'k', 'm', 'n', 'p', 'q', 'r', 'v', 'w', 'x', 'y']


# -------------데이터 전처리
# 문자를 숫자로 바꿉니다.
char_to_num = layers.StringLookup(vocabulary=list(characters), mask_token=None)

# 숫자를 문자로 바꿉니다.
num_to_char = layers.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), mask_token=None, invert=True
)

# data를 trian set과 validation set으로 나눈다.
def split_data(images, labels, train_size=0.9, shuffle=True):
    size = len(images)
    indices = tf.range(size)
    if shuffle:
        indices = tf.random.shuffle(indices)
    train_samples = int(size * train_size)
    x_train, y_train = images[indices[:train_samples]], labels[indices[:train_samples]]
    x_valid, y_valid = images[indices[train_samples:]], labels[indices[train_samples:]]
    return x_train, x_valid, y_train, y_valid

# 데이터 분할
x_train, x_valid, y_train, y_valid = split_data(np.array(images), np.array(labels))

# pad_sequences를 사용하는 함수
def pad_labels(labels, max_length):
    labels = tf.numpy_function(
        func=lambda x: pad_sequences([x], maxlen=max_length, padding='post')[0],
        inp=[labels],
        Tout=tf.int32
    )
    return labels

# 아래에서 데이터셋을 만들 때, 적용될 함수를 정의합시다.
def encode_single_sample(img_path, label):

    # 1. 이미지를 불러옵시다.
    img = tf.io.read_file(img_path)
    # 2. png 이미지로 변환하고, 해당 이미지를 grayscale로 변환합시다.
    img = tf.io.decode_png(img, channels=1)
    # 3. [0, 255]의 정수 범위를 [0, 1]의 실수 범위로 바꿉시다.
    img = tf.image.convert_image_dtype(img, tf.float32)
    # 4. 위에서 정한 이미지 사이즈로 resize합시다.
    img = tf.image.resize(img, [img_height, img_width])
    # 5.  5. 이미지와 가로와 세로를 뒤바꿉시다.
    # 우리는 이미지의 가로와 시간차원을 대응시키고 싶기 때문입니다.
    img = tf.transpose(img, perm=[1, 0, 2])
    # 6. 라벨값의 문자를 숫자로 바꿉시다.
    label = char_to_num(tf.strings.unicode_split(label, input_encoding='UTF-8'))
    # 7. padding을 적용하여 고정된 길이로 맞춥니다.
    # 7. 패딩을 추가합니다 (텐서를 넘파이 함수로 변환)
    label = pad_labels(label, max_length)

    return {"image": img, "label": label}


train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
train_dataset = (
    train_dataset.map( # 위에서 정의한 함수를 적용합니다.
        encode_single_sample, num_parallel_calls=tf.data.experimental.AUTOTUNE
    )
    .batch(batch_size) # 배치 사이즈를 지정합니다.
    .prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
)

validation_dataset = tf.data.Dataset.from_tensor_slices((x_valid, y_valid))
validation_dataset = (
    validation_dataset.map(
        encode_single_sample, num_parallel_calls=tf.data.experimental.AUTOTUNE
    )
    .batch(batch_size)
    .prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
)

#------------------데이터 시각화
# _, ax = plt.subplots(4, 4, figsize=(10, 5))
# for batch in train_dataset.take(1):
#     images = batch["image"]
#     labels = batch["label"]
#     for i in range(16):
#         img = (images[i] * 255).numpy().astype("uint8")
#         label = tf.strings.reduce_join(num_to_char(labels[i])).numpy().decode("utf-8")
#         ax[i // 4, i % 4].imshow(img[:, :, 0].T, cmap="gray")
#         ax[i // 4, i % 4].set_title(label)
#         ax[i // 4, i % 4].axis("off")
# plt.show()


#------------------모델정의
class CTCLayer(layers.Layer):
    def __init__(self, name=None):
        super().__init__(name=name)
        self.loss_fn = keras.backend.ctc_batch_cost

    def call(self, y_true, y_pred):
        # 모델이 training하는 경우, `self.add_loss()`를 사용하여 loss를 계산하고 더해줍니다.
        batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
        input_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
        label_length = tf.cast(tf.shape(y_true)[1], dtype="int64")

        input_length = input_length * tf.ones(shape=(batch_len, 1), dtype="int64")
        label_length = label_length * tf.ones(shape=(batch_len, 1), dtype="int64")

        loss = self.loss_fn(y_true, y_pred, input_length, label_length)
        self.add_loss(loss)
        # 테스트 시에는, 단지 예측 결과값만 반환합니다.
        return y_pred

def build_model():
     # 모델 input 정의
    input_img = layers.Input(shape=(img_width, img_height, 1), name="image", dtype="float32")
    labels = layers.Input(name="label", shape=(None,), dtype="float32")


    # 첫번째 conv block
    x = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_initializer="he_normal",
        padding="same",
        name="Conv1",
    )(input_img)
    x = layers.MaxPooling2D((2, 2), name="pool1")(x)

    # 두번째 conv block
    x = layers.Conv2D(
        64,
        (3, 3),
        activation="relu",
        kernel_initializer="he_normal",
        padding="same",
        name="Conv2",
    )(x)
    x = layers.MaxPooling2D((2, 2), name="pool2")(x)

    # 우리는 두 번의 max pool(stride 2, pool size 2)을 사용할 것입니다.
    # 그러므로 feature maps는 4배 downsampled 됩니다.
    # 마지막 레이어의 필터의 갯수는 64개입니다
    # 모델의 RNN part에 넣기 전에 Reshape를 해줍시다.

    new_shape = ((img_width // downsample_factor), (img_height // downsample_factor) * 64)
    x = layers.Reshape(target_shape=new_shape, name="reshape")(x)
    x = layers.Dense(64, activation="relu", name="dense1")(x)
    x = layers.Dropout(0.2)(x)

    # RNNs
    x = layers.Bidirectional(layers.LSTM(128, return_sequences=True, dropout=0.25))(x)
    x = layers.Bidirectional(layers.LSTM(64, return_sequences=True, dropout=0.25))(x)

    # Output layer
    x = layers.Dense(len(char_to_num.get_vocabulary()) + 1, activation="softmax", name="dense2")(x)

    # 위에서 제작한 CTC loss를 계산하는 CTC layer를 추가합시다.
    output = CTCLayer(name="ctc_loss")(labels, x)

    # 모델 정의
    model = keras.models.Model(inputs=[input_img, labels], outputs=output, name="ocr_model_v1")
    # 옵티마이저 정의
    opt = keras.optimizers.Adam()
    # 모델 컴파일
    model.compile(optimizer=opt)
    return model

model = build_model()
model.summary()


# ---------------------모델 트레이닝
epochs = 100
early_stopping_patience = 10

# early_stopping 콜백 함수 선언
early_stopping = keras.callbacks.EarlyStopping(
    monitor="val_loss", patience=early_stopping_patience, restore_best_weights=True
)

# 모델 훈련하기
history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=epochs,
    callbacks=[early_stopping],
)

# ---------------------모델 예측
# Get the prediction model by extracting layers till the output layer
# 출력 레이어까지 레이어를 추출하여 예측 모델을 가져옵니다.
prediction_model = keras.models.Model(
    model.get_layer(name="image").input, model.get_layer(name="dense2").output
)
prediction_model.summary()

# 출력값을 디코딩하는 함수 지정(output은 숫자로 나오기 때문에 위에서 지정한 num_to_char를 이용해서 문자로 변환
def decode_batch_predictions(pred):
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    # Use greedy search. For complex tasks, you can use beam search
    results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][
        :, :max_length
    ]
    # Iterate over the results and get back the text
    output_text = []
    for res in results:
        res = tf.strings.reduce_join(num_to_char(res)).numpy().decode("utf-8")
        output_text.append(res)
    return output_text

# ------------------------예측결과 확인하기
#  validation_dataset의 배치 1개를 시각화
for batch in validation_dataset.take(1):
    batch_images = batch["image"]
    batch_labels = batch["label"]

    preds = prediction_model.predict(batch_images)
    pred_texts = decode_batch_predictions(preds)

    orig_texts = []
    for label in batch_labels:
        label = tf.strings.reduce_join(num_to_char(label)).numpy().decode("utf-8")
        orig_texts.append(label)

    _, ax = plt.subplots(4, 4, figsize=(15, 5))
    for i in range(len(pred_texts)):
        img = (batch_images[i, :, :, 0] * 255).numpy().astype(np.uint8)
        img = img.T
        title = f"Prediction: {pred_texts[i]}"
        ax[i // 4, i % 4].imshow(img, cmap="gray")
        ax[i // 4, i % 4].set_title(title)
        ax[i // 4, i % 4].axis("off")
plt.show()
