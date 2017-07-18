#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import cv2
from matplotlib import pyplot as plt
from PIL import Image
from PIL.ExifTags import TAGS

SS_DEFAULT_SCALE = 30.0

class SSImage(object):
  def __init__(self, fname):
    super(SSImage, self).__init__()
    self.fname = fname
    self.image = cv2.imread(fname, cv2.IMREAD_UNCHANGED)

  def size(self):
    shape = self.image.shape
    print(shape)
    return (shape[1], shape[0])

  def date(self):
    image = Image.open(self.fname)
    exif = image._getexif()
    return (str)(exif[36867])

  def rawImage(self):
    return self.image
    
  def addTimestamp(timeStamp):
    pass
    
class SSTimestamp(object):
  def __init__(self):
    self.font = cv2.FONT_HERSHEY_SIMPLEX
    #字体scale可以设置为图片高度的1/10
    self.fontScale = 1
    self.color = (0, 0, 0) #bgr
    self.thickness = 3

  def process(self, image):
    imageWidth, imageHeight = image.size()
    print(imageWidth)
    print(imageHeight)
    text = image.date()
    textSize = cv2.getTextSize(text, self.font, self.fontScale, self.thickness)
    height = textSize[0][1]
    print(textSize)
    print(height)
    desiredFontHeight = imageHeight / SS_DEFAULT_SCALE
    self.fontScale = (int)(desiredFontHeight / height)
    self.thickness = self.thickness * self.fontScale

    #right margin = bottom margin = desiredFontHeight
    textSize = cv2.getTextSize(text, self.font, self.fontScale, self.thickness)
    width = textSize[0][0]
    print(textSize)
    print(width)
    position = ((int)(imageWidth - width - desiredFontHeight), (int)(imageHeight - desiredFontHeight))
    rawImage = image.rawImage()
    print(position)
    print(self.fontScale)
    cv2.putText(rawImage, text, position, self.font, self.fontScale, self.color, self.thickness ,cv2.LINE_AA)

    return rawImage

testImage = SSImage('1.jpg')
timeStamp = SSTimestamp()
result = timeStamp.process(testImage)
showImage = result[:,:,::-1]



plt.imshow(showImage)
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()
