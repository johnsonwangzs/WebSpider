# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-21
# @file    : tesserocr_usage.py
# @function: OCR识别图形验证码。

import tesserocr
from PIL import Image
import numpy as np

image = Image.open('captcha.png')  # 新建一个图片对象
result = tesserocr.image_to_text(image)  # 将图片转为文本
print(result)
print(tesserocr.file_to_text('captcha.png'))  # 直接将图片文件转为字符串
print('='*32)

# ========为了解决图片识别不佳的问题，对图片做处理========
image = Image.open('captcha2.png')
print(np.array(image).shape)  # (38,112,4):高，宽，每个像素点的表示向量（长度为4的数组，RGBA）
print(image.mode)  # mode：定义了图片的类型和像素的位宽，共9种。（RGBA:有透明通道的真彩色）

image = image.convert('L')  # 把mode由RGBA转为更简单的L（灰度图像）
# image.show()
threshold = 100  # 设定灰度阈值
array = np.array(image)  # 将图片转为numpy数组
array = np.where(array > threshold, 255, 0)  # 对数组进行筛选和处理（将灰度大于阈值的图片的像素设为255表示白色，反之设为0表示黑色）
image = Image.fromarray(array.astype('uint8'))
image.show()
print(tesserocr.image_to_text(image))
