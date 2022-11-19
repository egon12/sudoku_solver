import numpy as np
import os
import sys
from input import names

def rename(name):
    d = np.loadtxt(f"class/{name}.class.txt", dtype=str, delimiter=";")
    m = map(lambda x: x[1] + "__" + x[0], d)
    m = list(m)

    for i in range(len(d)):
        os.rename(f"./images/{d[i][0]}", f"./images/{m[i]}")

def all():
    for name in names():
        rename(name)

def main():
    if len(sys.argv) < 2:
        print("Usage: predict.py <boardname>")
        return
    rename(sys.argv[1])

if __name__ == "__main__":
    #main()
    all()

