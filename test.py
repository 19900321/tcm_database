# Import the necessary packages
import cv2
import numpy as np
import numpy as np

def back_rm(filename):
    # Load the image
    img = cv2.imread(filename)

    # Convert the image to grayscale
    gr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



    # Make a copy of the grayscale image
    bg = gr.copy()

    # Apply morphological transformations
    for i in range(5):
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                            (2 * i + 1, 2 * i + 1))
        bg = cv2.morphologyEx(bg, cv2.MORPH_CLOSE, kernel2)
        bg = cv2.morphologyEx(bg, cv2.MORPH_OPEN, kernel2)

    # Subtract the grayscale image from its processed copy
    dif = cv2.subtract(bg, gr)

    # Apply thresholding
    bw = cv2.threshold(dif, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    dark = cv2.threshold(bg, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Extract pixels in the dark region
    darkpix = gr[np.where(dark > 0)]

    # Threshold the dark region to get the darker pixels inside it
    darkpix = cv2.threshold(darkpix, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Paste the extracted darker pixels in the watermark region
    bw[np.where(dark > 0)] = darkpix.T

    alpha = 2.0
    beta = -160

    new = alpha * img + beta
    new = np.clip(new, 0, 255).astype(np.uint8)

    cv2.imwrite('original_data/final.jpg', bw)



# imgs = io.imread('./test.png')
# io.imsave('./hh.png',imgs)
# imgs = np.array(imgs)
# print(imgs.shape)
# r = []
# g = []
# b = []
# alpha = []

def judge(x,y):
    temp = -(600.0/1575.0) * x
    if y > 1350 + temp and y < 1500 + temp:
        return True
    else:
        return False

# for  i in range(imgs.shape[0]):
#     for j in range(imgs.shape[1]):
#         if not judge(j,i):
#             continue
#         if imgs[i][j][1] > 100 and imgs[i][j][1] < 250 and imgs[i][j][2] > 100 and imgs[i][j][2] < 250:
#             imgs[i][j][0] =  imgs[i][j][1] = imgs[i][j][2] = 255
#         if imgs[i][j][1] < 10 and imgs[i][j][2] < 100:
#             imgs[i][j][0] =  imgs[i][j][1] = imgs[i][j][2] = 0

# io.imsave('./hh.png',imgs)
# print(r)
# print(g)
# print(b)
# print(alpha)

def select_pixel(r,g,b):
    if (r == 208 and g == 208 and b == 208 ) or (r == 196 and g == 196 and b == 196) \
        or (r == 206 and g == 206 and b == 206 ):
        return True
    else:
        return False
def select_pixel2(r,g,b):
    if r > 175 and r < 250 and g > 175 and g < 250 and b > 175 and b < 250:
        return True
    else:
        return False
def handle(imgs):
    for  i in range(imgs.shape[0]):
        for j in range(imgs.shape[1]):
            # if not judge(j,i):
            #     continue
            # if imgs[i][j][1] > 100 and imgs[i][j][1] < 250 and imgs[i][j][2] > 100 and imgs[i][j][2] < 250:
            if select_pixel2(imgs[i][j][0],imgs[i][j][1],imgs[i][j][2]):
                imgs[i][j][0] =  imgs[i][j][1] = imgs[i][j][2] = 255
            # if not select_pixel(imgs[i][j][0],imgs[i][j][1],imgs[i][j][2]):
            #     imgs[i][j][0] =  imgs[i][j][1] = imgs[i][j][2] = 0
    return imgs

img_2  = handle(img)
filename = 'original_data/Image from iOS.jpg'
back_rm('original_data/Image from iOS.jpg')