import sys
import tensorflow as tf
import numpy as np

from PIL import Image


model = tf.keras.models.load_model("second.mod")

def filename(basename, x, y):
    return "images/" + basename + "_" + str(y) + str(x) + ".png"

def oneboard(name):
    res = []
    for y in range(9):
        for x in range(9):
            res.append(onenumber(filename(name, x, y)))
    return np.array(res)

def onenumber(filename):
    img = Image.open(filename)
    img = img.resize((28,28))
    img = np.array(img)
    return img

def predict(name):
    res = model.predict(oneboard(name))
    res = np.argmax(res, axis=1)
    for y in range(9):
        for x in range(9):
            print(filename(name, x, y) + ";" + str(res[y*9+x]))

def main():
    if len(sys.argv) < 2:
        print("Usage: predict.py <boardname>")
        return
    predict(sys.argv[1])

if __name__ == "__main__":
    main()

