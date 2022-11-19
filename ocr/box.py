from pathlib import Path
from PIL import Image
import numpy as np
from input import names

def main():
    for name in names():
        split_image(f"images/{name}.png")

def split_image(filename):
    # Split the image into 9 boxes
    # filename: name of the image file
    img = Image.open(filename).convert("L")
    img = np.array(img)
    
    p = Path(filename)
    for y in range(3):
        for x in range(3):
            onebox = box(img, y, x)
            for i in range(3):
                for j in range(3):
                    onenumber = box(onebox, i, j)
                    n1 = y*3+i
                    n2 = x*3+j
                    Image.fromarray(onenumber).save(p.parent / f"{p.stem}_{n1}{n2}.png")


def box(img, row, col):
    # Return the 1 box of 9 number 
    # img: 3D array of pixels
    # row, col: coordinates of the pixel
    # returns: 3D array of pixels

    hw = img.shape[0] // 3
    bw = img.shape[1] // 3

    return img[row*hw:(row+1)*hw, col*bw:(col+1)*bw]


if __name__ == "__main__":
    main()
