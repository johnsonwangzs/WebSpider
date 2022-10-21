# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-21
# @file    : opencv_demo.py
# @function: OpenCV识别实战
"""
利用OpenCV识别滑动验证码，自动登录
"""

import cv2

GAUSSIAN_BLUR_KERNEL_SIZE = (5, 5)
GAUSSIAN_BLUR_SIGMA_X = 0
CANNY_THRESHOLD1 = 200
CANNY_THRESHOLD2 = 450


def get_gaussian_blur_image(image):
    """
    高斯滤波
    :param image:待处理图片
    :return: 高斯滤波处理后的图片信息
    """
    return cv2.GaussianBlur(image, GAUSSIAN_BLUR_KERNEL_SIZE, GAUSSIAN_BLUR_SIGMA_X)


def get_canny_image(image):
    """
    边缘检测
    :param image: 待处理图片
    :return: 边缘检测处理后的图片信息
    """
    return cv2.Canny(image, CANNY_THRESHOLD1, CANNY_THRESHOLD2)


def get_contours(image):
    """
    轮廓提取
    :param image: 待处理图片
    :return: 提取得到的轮廓信息
    """
    contours, _ = cv2.findContours(image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def get_contour_area_threshold(image_width, image_height):
    """
    根据轮廓的外接矩形面积筛选结果
    测量得到目标缺口的外接矩形的高度约验证码高度的0.25倍，宽度约验证码宽度的0.15倍
    定义目标轮廓的面积下限和面积上限。允许误差20%
    :param image_width:
    :param image_height:
    :return:
    """
    contour_area_min = (image_width * 0.15) * (image_height * 0.25) * 0.8
    contour_area_max = (image_width * 0.15) * (image_height * 0.25) * 1.2
    return contour_area_min, contour_area_max


def get_arc_length_threshold(image_width, image_height):
    """
    根据轮廓的外接矩形周长筛选结果
    测量得到目标缺口的外接矩形的高度约验证码高度的0.25倍，宽度约验证码宽度的0.15倍
    定义目标轮廓的周长下限和周长上限。允许误差20%
    :param image_width:
    :param image_height:
    :return:
    """
    arc_length_min = ((image_width * 0.15) + (image_height * 0.25)) * 2 * 0.8
    arc_length_max = ((image_width * 0.15) + (image_height * 0.25)) * 2 * 1.2
    return arc_length_min, arc_length_max


def get_offset_threshold(image_width):
    """
    定义缺口位置（左侧）的偏移量下限和偏移量上限
    :param image_width:
    :return:
    """
    offset_min = 0.2 * image_width
    offset_max = 0.85 * image_width
    return offset_min, offset_max


image_raw = cv2.imread('captcha.png')  # 原始图片
image_height, image_width, _ = image_raw.shape
image_gaussian_blur = get_gaussian_blur_image(image_raw)  # 高斯滤波
image_canny = get_canny_image(image_gaussian_blur)  # 边缘检测
contours = get_contours(image_canny)  # 各个边缘的轮廓

contour_area_min, contour_area_max = get_contour_area_threshold(image_width, image_height)
arc_length_min, arc_length_max = get_arc_length_threshold(image_width, image_height)
offset_min, offset_max = get_offset_threshold(image_width)
offset = None
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if contour_area_min < cv2.contourArea(contour) < contour_area_max and \
            arc_length_min < cv2.arcLength(contour, True) < arc_length_max and \
            offset_min < x < offset_max:
        cv2.rectangle(image_raw, (x, y), (x + w, y + h), (0, 0, 255), 2)
        offset = x
cv2.imwrite('image_label.png', image_raw)
print('offset', offset)
