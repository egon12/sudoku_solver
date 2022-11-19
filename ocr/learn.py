import tensorflow as tf
import numpy as np
from PIL import Image


def loadimg():
    all = np.array([], dtype=np.float32)
    all = oneboard("img01")
    all = np.array(all)
    return all

def loadimage(name):
    res = []
    for y in range(9):
        for x in range(9):
            n = name + "_" + str(y) + str(x) + ".png"
            res.append(oneimg(n))
    return np.array(res)

def loadclass(name):
    d = np.loadtxt("class/" + name + ".class.txt", delimiter=";", dtype="U9")
    d = np.array(d[:,1], dtype=np.uint8)
    return d

def oneimg(path):
    img = Image.open("images/" + path).convert('L')
    img = img.resize((50, 50))
    img = np.array(img)
    img = img.astype(np.float32)
    img = np.multiply(img, 1.0 / 255.0)
    return img

def train(x_train, y_train):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(50,50)),
        tf.keras.layers.Dense(2500, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(1000, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10),
    ])

    predictions = model(x_train[:1]).numpy()

    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

    loss_fn(y_train[:1], predictions).numpy()

    model.compile(optimizer='adam', loss=loss_fn, metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=100)
    return model


x_train = loadimage("img01")
y_train = loadclass("img01")

for i in range(1, 23):
    num = str(i).rjust(2, '0')
    name = "img" + num
    x = loadimage(name)
    y = loadclass(name)
    x_train = np.concatenate((x_train, x))
    y_train = np.concatenate((y_train, y))

model = train(x_train, y_train)
model.save("six.h5")

