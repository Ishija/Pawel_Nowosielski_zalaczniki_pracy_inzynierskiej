import tensorflow as tf
import numpy as np

train_data_file = []
test_data_file = []
with open('training_data_100k.txt', 'r') as f:
    for line in f:
        line = line.strip().split()
        cards = [int(line[k]) for k in range(16)]
        winning_set = int(line[-1])
        train_data_file.append((cards, winning_set))

np.random.shuffle(train_data_file)

with open('test_data_100k.txt', 'r') as f:
    for line in f:
        line = line.strip().split()
        cards = [int(line[k]) for k in range(16)]
        winning_set = int(line[-1])
        test_data_file.append((cards, winning_set))

np.random.shuffle(test_data_file)

model = tf.keras.models.Sequential([
    tf.keras.layers.BatchNormalization(input_shape=(16,)),
    tf.keras.layers.Dense(1278, activation='relu'),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Dense(913, activation='relu'),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

x_train = np.array([drawn_cards for drawn_cards, _ in train_data_file])
y_train = np.array([winner for _, winner in train_data_file])
x_test = np.array([drawn_cards for drawn_cards, _ in test_data_file])
y_test = np.array([winner for _, winner in test_data_file])

model.fit(x_train, y_train, epochs=500, validation_data=(x_test, y_test), batch_size=64)
model.save('prediction_model_3_500e.h5')
model.summary()