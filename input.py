import sys
import tensorflow as tf
import numpy as np
from PIL import Image
from board import Board, Validation
from trim import trim, box

class StringInput:

    def __init__(self, string):
        self.string = string

    def read(self):
        board = Board()
        lines = self.string.splitlines()
        if len(lines) != 9:
            raise Exception("Invalid input, must be 9 lines")
        for i in range(9):
            line = lines[i]
            if len(line) != 9:
                raise Exception("Invalid input, line {} must be 9 characters long".format(i + 1))
            for j in range(9):
                c = line[j]
                if c == ' ':
                    board.board[i, j] = 0
                else:
                    board.board[i, j] = int(c)
        return board

class FileInput:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename, 'r') as f:
            return StringInput(f.read()).read()

class ImageInput:
    def __init__(self, filename):
        self.filename = filename
        self.model = tf.keras.models.load_model("ocr/second.mod")

    def read(self):
        imgs = self.get_numbers_image(self.filename)
        predictions = self.model.predict(imgs)
        num = predictions.argmax(axis=1)

        res = ""
        for i in range(9):
            line = list(num[0:9])
            res += ''.join(map(lambda x: str(x), line)) + '\n'
            num = num[9:]
        
        return StringInput(res).read()

    def get_numbers_image(self, filename):
        img = Image.open(filename).convert("L")
        img = np.array(img)
        img = trim(img)

        d = {}
        
        for y in range(3):
            for x in range(3):
                onebox = box(img, y, x)
                for i in range(3):
                    for j in range(3):
                        onenumber = box(onebox, i, j)
                        n1 = y*3+i
                        n2 = x*3+j
                        key = str(n1) + str(n2)
                        im = Image.fromarray(onenumber).resize((28, 28))
                        im.save("imgtmp/img{}.png".format(key))
                        im = np.array(im)
                        im = im.astype(np.float32)
                        im = np.multiply(im, 1.0 / 255.0)
                        d[key] = im

        res = []
        for y in range(9):
            for x in range(9):
                key = str(y) + str(x)
                res.append(d[key])
        return np.array(res)

