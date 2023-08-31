from functools import partial

import cv2

from poe.bulk.image_cutter import cut_image_to_frags, normalize_frag
from poe.bulk.predictions import predict_wrapper


def translate_path_to_prediction(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return predict_wrapper(gray)


def process_frag(img):
    try:
        return normalize_frag(img, target=(32, 80))
    except:
        return None


def main():
    path = "data/tabs/image1.png"
    img = cv2.imread(path)
    print(img)
    frags = cut_image_to_frags(img)
    normalized_frags = [[process_frag(column) for column in row] for row in frags]
    predicted_frags = [[None if column is None else predict_wrapper(column) for column in row] for row in
                       normalized_frags]
    print(predicted_frags)


if __name__ == '__main__':
    main()
