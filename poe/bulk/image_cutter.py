from itertools import groupby

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def remove_padding(img, padding=25):
    img = img[padding : img.shape[0] - padding, padding : img.shape[1] - padding]
    return img


def remove_almost_black_pixels(img):
    # mask=(img == (43, 38, 37))| (img == (32, 29, 28))
    # img[mask]=0
    # print(img.shape)
    # mask = cv2.inRange(img,(0,0,0),(10,41,13))
    # cv2.imwrite('mask.png',mask)
    # img[mask]=0

    # for g in range(25,40):
    #     mask|=img == (0, g, 0)
    # img[mask]=0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray[gray < 50] = 0
    return gray


def define_x_cuts(gray):
    dilatation_size = 2
    element = cv2.getStructuringElement(
        cv2.MORPH_RECT, (2 * dilatation_size + 1, 2 * dilatation_size + 1), (dilatation_size, dilatation_size)
    )
    gray = cv2.dilate(gray, element)

    col_mean_values = gray.mean(axis=0)
    col_mean_values = np.array([v if v > 0 else 0 for v in col_mean_values])
    x_cuts = [
        int(np.mean(list(y[0][0] for y in v)))
        for k, v in groupby(np.ndenumerate(col_mean_values), key=lambda x: x[1])
        if k == 0
    ]
    _ = pd.Series(col_mean_values).plot(figsize=(20, 5))
    return x_cuts


def define_y_cuts(gray):
    row_mean_values = gray.mean(axis=1)
    y_cuts = [
        int(np.mean(list(y[0][0] for y in v)))
        for k, v in groupby(np.ndenumerate(row_mean_values), key=lambda x: x[1])
        if k == 0
    ]
    _ = pd.Series(row_mean_values).plot(figsize=(20, 5))

    return y_cuts


def draw_lines(img, y_cuts, x_cuts):
    img = np.copy(img)
    result_lines = []
    for i,y in enumerate(y_cuts):
        result_lines.append(((0, y), (img.shape[1], y), 255, 1))
        cv2.putText(img,str(i),(100,y-5),cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=255)
    for i,x in enumerate(x_cuts):
        result_lines.append(((x, 0), (x, img.shape[0]), 255, 1))
        cv2.putText(img,str(i+1),(x,75),cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=255)

    for line in result_lines:
        cv2.line(img, *line)
    plt.figure(figsize=(20, 20))

    _ = plt.imshow(img)
    cv2.imwrite("debuglines.png", img)


def remove_whitespace():
    pass


def cut_into_frags(img, y_cuts, x_cuts):
    frags = [
        [img[y0 + 1 : y1, x0 + 1 : x1] for i, (y0, y1) in enumerate(zip([0] + y_cuts, y_cuts))]
        for j, (x0, x1) in enumerate(zip([0] + x_cuts, x_cuts))
    ]
    return frags


def cut_image(img):
    img = remove_padding(img, 25)
    img = remove_almost_black_pixels(img)
    cv2.imwrite("debug.png", img)
    debug=np.copy(img)
    debug[debug>0]=255
    cv2.imwrite("debugbw.png", debug)
    y_cuts = define_y_cuts(img)
    img = img[y_cuts[4] :, :]
    y_cuts = [y - y_cuts[4] for y in y_cuts][5:]
    x_cuts = define_x_cuts(img)
    return img, y_cuts, x_cuts


def normalize_frag(img,target=(32,80)):
    img =img
    # gray = 255*(gray < 128).astype(np.uint8) # To invert the text to white
    coords = cv2.findNonZero(img)  # Find all non-zero points (text)
    x, y, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box
    rect = img[y : y + h, x : x + w]
    top= int((target[0]-rect.shape[0])/2)
    bottom=target[0]-rect.shape[0]-top
    left=int((target[1]-rect.shape[1])/2)
    right= target[1] - rect.shape[1] - left
    final = cv2.copyMakeBorder(rect, top, bottom, left, right, cv2.BORDER_CONSTANT)
    assert final.shape[:2]==target,final.shape
    return 255-final


def cut_image_to_frags(img):
    img, y_cuts, x_cuts = cut_image(img)
    draw_lines(img, y_cuts, x_cuts)
    frags = cut_into_frags(img, y_cuts, x_cuts)
    return frags
if __name__ == '__main__':
    path = 'data/tabs/unknown (30).png'

    img = cv2.imread(path)
    print(img)
    frags=cut_image_to_frags(img)
    pass