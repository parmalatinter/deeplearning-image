# ref : https://qiita.com/best_not_best/items/c9497ffb5240622ede01

# !/usr/bin/env python
# -*- coding: UTF-8 -*-

"""hist matching."""

import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

TARGET_FILE = 'compare.jpg'
IMG_DIR = os.path.abspath(os.path.dirname(__file__)) + '/images/tests/'
IMG_BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + '/images/base/'
IMG_RESULT_DIR = os.path.abspath(os.path.dirname(__file__)) + '/images/result/'
IMG_NEW_DIR = os.path.abspath(os.path.dirname(__file__)) + '/images/new/'
bgrLower = (10, 10, 10)  # 抽出する色の下限
bgrUpper = (100, 100, 88)  # 抽出する色の上限


# BGRで特定の色を抽出する関数
def bgr_extraction(image):
    # HSV に変換する。
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 2値化する。
    dst = cv2.inRange(hsv, (0, 0, 0), (64, 94, 255))

    fig, ax = plt.subplots(facecolor="w")
    ax.imshow(dst, cmap="gray")

    # plt.show()

    # cv2.imwrite(IMG_RESULT_DIR + 'figure2.png', dst)

    return dst


def match(from_img, to_img, file_name):
    # Initiate ORB detector
    orb = cv2.ORB_create()

    # find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(from_img, None)
    kp2, des2 = orb.detectAndCompute(to_img, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des1, des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)

    # # データを間引く
    # ratio = 0.2
    # good = []
    # for m, n in matches:
    #     if m.distance < ratio * n.distance:
    #         good.append([m])

    print('there are %d good matches' % (len(matches)))

    # Draw first 10 matches.
    img3 = cv2.drawMatches(from_img, kp1, to_img, kp2, matches[:100], None, flags=2)

    # plt.imshow(img3), plt.show()

    cv2.imwrite(IMG_RESULT_DIR + file_name, img3)


def compare_histogram(target_hist, to_img):
    comparing_hist = cv2.calcHist([to_img], [0], None, [256], [0, 256])

    ret = cv2.compareHist(target_hist, comparing_hist, 0)

    return ret


def compare_detection(bf: object, detector: object, target_kp: object,
                      target_des: object, target_img: object, comparing_img: object) -> object:
    try:

        (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
        # Brute-Force Matcherの生成
        bf = cv2.BFMatcher()

        # 特徴量ベクトル同士をBrute-Force＆KNNでマッチング
        matches = bf.knnMatch(target_des, comparing_des, k=2)

        # dist = [m.distance for m in matches]


        # データを間引く
        ratio = 1
        good = []
        for m, n in matches:
            if m.distance < ratio * n.distance:
                good.append([m])

        dist = 'there are %d good matches' % (len(good))

        # 対応する特徴点同士を描画
        img = cv2.drawMatchesKnn(target_img, target_kp, comparing_img, comparing_kp, good[:2], None, flags=2)
    except cv2.error:
        dist = ''
        img = comparing_img

    plt.imshow(img), plt.show()
    return dist, img


def compare(num=0):
    IMG_SIZE_BASE = (90, 240)
    IMG_SIZE = (600, 800)

    target_img_path = IMG_BASE_DIR + TARGET_FILE
    target_img = cv2.imread(target_img_path)
    target_img = cv2.resize(target_img, IMG_SIZE)
    target_img = bgr_extraction(target_img)
    target_hist = cv2.calcHist([target_img], [0], None, [256], [0, 256])

    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    detector = cv2.AKAZE_create()
    (target_kp, target_des) = detector.detectAndCompute(target_img, None)

    print('TARGET_FILE: %s' % TARGET_FILE)

    try:
        files = os.listdir(IMG_DIR)
        for file in files:
            if file == '.DS_Store' or file == TARGET_FILE:
                continue

            comparing_img_path = IMG_DIR + file
            comparing_img = cv2.imread(comparing_img_path)
            comparing_img = cv2.resize(comparing_img, IMG_SIZE)
            comparing_img = bgr_extraction(comparing_img)

            print(comparing_img_path)
            print(file, compare_histogram(target_hist, comparing_img))
            # res, image = compare_detection(bf, detector, target_kp, target_des, target_img, comparing_img)
            # print(file, res)

            match(target_img, comparing_img, file)
            # break
    except KeyboardInterrupt:
        print("Ctrl+Cで停止しました")
        exit()


if __name__ == '__main__':
    compare()
