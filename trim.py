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
