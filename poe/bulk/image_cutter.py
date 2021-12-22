from itertools import groupby

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def remove_padding(img, padding=25):
    img = img[padding : img.shape[0] - padding, padding : img.shape[1] - padding]
    return img


def remove_almost_black_pixels(img):
    img[img == (43, 38, 37)] *= 0
    img[img == (32, 29, 28)] *= 0
    img[img == (3, 1, 1)] *= 0
    img[img == (4, 2, 0)] *= 0
    img[img == (44, 0, 1)] *= 0
    img[img == (41, 0, 1)] *= 0
    img[img == (42, 0, 0)] *= 0
    img[img == (40, 1, 1)] *= 0
    img[img == (40, 0, 36)] *= 0
    img[img == (40, 0, 37)] *= 0
    img[img == (40, 0, 38)] *= 0
    img[img == (41, 0, 36)] *= 0
    img[img == (41, 0, 37)] *= 0
    img[img == (41, 0, 38)] *= 0
    img[img == (39, 0, 36)] *= 0
    img[img == (39, 0, 37)] *= 0
    img[img == (39, 0, 38)] *= 0
    for g in range(40):
        img[img == (0, g, 0)] *= 0
    img[img.sum(axis=2) < 8] *= 0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img[gray < 30] = 0
    print(img[gray < 30].sum())
    return img


def define_x_cuts(img):
    dilatation_size = 1
    element = cv2.getStructuringElement(
        cv2.MORPH_RECT, (2 * dilatation_size + 1, 2 * dilatation_size + 1), (dilatation_size, dilatation_size)
    )
    img = cv2.dilate(img, element)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    col_mean_values = gray.mean(axis=0)
    col_mean_values = np.array([v if v > 0 else 0 for v in col_mean_values])
    x_cuts = [
        int(np.mean(list(y[0][0] for y in v)))
        for k, v in groupby(np.ndenumerate(col_mean_values), key=lambda x: x[1])
        if k == 0
    ]
    _ = pd.Series(col_mean_values).plot(figsize=(20, 5))
    return x_cuts


def define_y_cuts(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray[gray < 5] = 0
    row_mean_values = gray.mean(axis=1)
    y_cuts = [
        int(np.mean(list(y[0][0] for y in v)))
        for k, v in groupby(np.ndenumerate(row_mean_values), key=lambda x: x[1])
        if k == 0
    ]
    _ = pd.Series(row_mean_values).plot(figsize=(20, 5))

    return y_cuts


def draw_lines(img, y_cuts, x_cuts):
    img = img[...]
    result_lines = []
    for y in y_cuts:
        result_lines.append(((0, y), (img.shape[1], y), (0, 0, 255), 1))
    for x in x_cuts:
        result_lines.append(((x, 0), (x, img.shape[0]), (0, 0, 255), 1))

    for line in result_lines:
        cv2.line(img, *line)
    plt.figure(figsize=(20, 20))

    _ = plt.imshow(img)


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
    y_cuts = define_y_cuts(img)
    img = img[y_cuts[4] :, :]
    y_cuts = [y - y_cuts[4] for y in y_cuts][5:]
    x_cuts = define_x_cuts(img)
    return img, y_cuts, x_cuts


def normalize_frag(img,target=(32,80)):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray = 255*(gray < 128).astype(np.uint8) # To invert the text to white
    coords = cv2.findNonZero(gray)  # Find all non-zero points (text)
    x, y, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box
    rect = img[y : y + h, x : x + w]
    top= int((target[0]-rect.shape[0])/2)
    bottom=target[0]-rect.shape[0]-top
    left=int((target[1]-rect.shape[1])/2)
    right= target[1] - rect.shape[1] - left
    final = cv2.copyMakeBorder(rect, top, bottom, left, right, cv2.BORDER_CONSTANT)
    assert final.shape[:2]==target,final.shape
    return 255-cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)


def cut_image_to_frags(img):
    img, y_cuts, x_cuts = cut_image(img)
    draw_lines(img, y_cuts, x_cuts)
    frags = cut_into_frags(img, y_cuts, x_cuts)
    return frags
