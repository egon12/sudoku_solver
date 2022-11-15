from PIL import Image
import numpy as np

def main():
    trim_img("images/img01.png")
    trim_img("images/img02.png")
    trim_img("images/img03.png")
    trim_img("images/img03.png")
    trim_img("images/img04.png")
    trim_img("images/img05.png")
    trim_img("images/img06.png")
    trim_img("images/img07.png")
    trim_img("images/img08.png")
    trim_img("images/img09.png")
    trim_img("images/img10.png")

def trim_img(filename):
    img = Image.open(filename).convert('L')
    img = np.array(img)
    img = trim(img)
    img = Image.fromarray(img)
    img.save(filename)


def trim(img):
    # Trim the image to the smallest rectangle that contains all non-white pixels
    # img: 3D array of pixels
    # returns: 3D array of pixels

    # Find the first and last non-white pixels in each column
    top = 0
    for i in range(img.shape[0]):
        if (img[i, :] != 255).any():
            top = i
            break

    bottom = 0
    for i in range(img.shape[0]-1, 0, -1):
        if (img[i, :] != 255).any():
            bottom = i
            break

    # Find the first and last non-white pixels in each row
    first = 0
    for i in range(img.shape[1]):
        if (img[:, i] != 255).any():
            first = i
            break

    last = 0
    for i in range(img.shape[1]-1, 0, -1):
        if (img[:, i] != 255).any():
            last = i
            break

    # Crop the image using the coordinates of these pixels
    return img[top:bottom, first:last]


if __name__ == "__main__":
    main()

