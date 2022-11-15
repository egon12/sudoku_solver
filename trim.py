from PIL import Image
import numpy as np

def main():
    img = Image.open('screen.png').convert('L')
    img = np.array(img)
    img = trim(img)
    img = Image.fromarray(img)
    img.save('screen_trim.png')

    img = np.array(img)
    img = box(img, 0, 2)
    img = Image.fromarray(img)
    img.save('screen_box.png')

    img = np.array(img)
    img1 = box(img, 0, 0)
    img1 = Image.fromarray(img1)
    img1.save('screen_box_1.png')

    img5 = box(img, 1, 1)
    img5= Image.fromarray(img5)
    img5.save('screen_box_5.png')

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

def box(img, row, col):
    # Return the 1 box of 9 number 
    # img: 3D array of pixels
    # row, col: coordinates of the pixel
    # returns: 3D array of pixels

    hw = img.shape[0] // 3
    bw = img.shape[1] // 3

    return img[row*hw:(row+1)*hw, col*bw:(col+1)*bw]
    
if __name__ == '__main__':
    main()
