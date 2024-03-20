import json
import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, Dropout

data_list = {"black": [], "white": []}

for folder in ["black", "white"]:
    for filename in os.listdir(f"./shobu_dataset/{folder}/"):
        if filename.endswith(".json"):
            file_path = os.path.join(f"./shobu_dataset/{folder}/", filename)
            with open(file_path, 'r') as file:
                json_data = json.load(file)
                data_list[folder].append(json_data)

X = []
y = []
for game in data_list['white']:
    board_states = game['game_states']
    winner = 0
    for state in board_states:
        board = np.zeros((8, 8))
        for i in range(8):
            for j in range(8):
                if state['board'][i * 8 + j] == 'x':
                    board[i][j] = -1
                elif state['board'][i * 8 + j] == 'o':
                    board[i][j] = 1
                else:
                    board[i][j] = 0
        X.append(board)
        y.append(winner)

for game in data_list['black']:
    board_states = game['game_states']
    winner = 1
    for state in board_states:
        board = np.zeros((8, 8))
        for i in range(8):
            for j in range(8):
                if state['board'][i * 8 + j] == 'x':
                    board[i][j] = -1
                elif state['board'][i * 8 + j] == 'o':
                    board[i][j] = 1
                else:
                    board[i][j] = 0
        X.append(board)
        y.append(winner)

X = np.array(X)
y = np.array(y)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Sequential([
    Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(8, 8, 1)),
    Conv2D(64, (3, 3), activation='relu'),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=2, batch_size=32, validation_data=(X_test, y_test))

loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Accuracy: {accuracy}')

model.save('shobu_winner_prediction_model.h5')