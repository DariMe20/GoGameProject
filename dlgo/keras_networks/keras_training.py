import numpy as np
from keras import Sequential
from keras.layers import Conv2D, Dropout, MaxPooling2D, Flatten, Dense
import os
from keras.optimizers import Adagrad

np.random.seed(123)
X = np.load('C:/DARIA/1.FSEGA/LICENTA/GoGameProject/features-40k.npy')
Y = np.load('C:/DARIA/1.FSEGA/LICENTA/GoGameProject/labels-40k.npy')
samples = X.shape[0]
size = 9
input_shape = (size, size, 1)

X = X.reshape(samples, size, size, 1)
train_samples = int(0.9 * samples)
X_train, X_test = X[:train_samples], X[train_samples:]
Y_train, Y_test = Y[:train_samples], Y[train_samples:]

model = Sequential()

# DOUA LAYERE CONVOLUTIONARE
model.add(Conv2D(48,
                 kernel_size=(3, 3),
                 activation='relu',
                 padding='same',
                 input_shape=input_shape))
model.add(Dropout(rate=0.5))

model.add(Conv2D(48,
                 (3, 3),
                 padding='same',
                 activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(rate=0.5))
model.add(Flatten())

# DOUA LAYERE DENSE
model.add(Dense(512, activation='relu'))
model.add(Dropout(rate=0.5))
model.add(Dense(size * size, activation='softmax'))

model.summary()
model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])

model.fit(X_train, Y_train,
          batch_size=64,
          epochs=150,
          verbose=1,
          validation_data=(X_test, Y_test))

score = model.evaluate(X_test, Y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

model_dir = '.\\'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

model_path = os.path.join(model_dir, 'model2.h5')
model.save(model_path)

print("Modelul a fost salvat cu succes")

def softmax(x):
    """

    :param x:
    :return:
    """
    e_x = np.exp(x)
    e_x_sum = np.sum(e_x)
    return e_x / e_x_sum

# test_board = np.array([[
#  0, 0, 0, 0, 0, 0, 0, 0, 0,
#  0, 0, 0, 0, 0, 0, 0, 0, 0,
#  0, 0, 0, 0, 0, 0, -1, 0, 0,
#  0, 0, 0, 0, 1, 0, 0, 0, 0,
#  0, 0, 0, 1, -1, 1, 0, 0, 0,
#  0, 0, 0, 0, 0, 0, 0, 0, 0,
#  0, 0, 0, 0, 0, 0, 0, 0, 0,
#  0, 0, 0, 0, 0, 0, 0, 0, 0,
#  0, 0, 0, 0, 0, 0, 0, 0, 0,
# ]])
# test_board_reshaped = test_board.reshape(-1, 9, 9, 1)  # Adaugă '-1' pentru batch size, care va fi inferat
# move_probs = model.predict(test_board_reshaped)[0]
# i = 0
# for row in range(9):
#     row_formatted = []
#     for col in range(9):
#         row_formatted.append('{:.3f}'.format(move_probs[i]))
#         i += 1  # Acesta trebuie să fie în interiorul buclei `for col`
#     print(' '.join(row_formatted))
