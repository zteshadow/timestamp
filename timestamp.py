#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import cv2
from matplotlib import pyplot as plt
from PIL import Image
from PIL.ExifTags import TAGS

SS_DEFAULT_SCALE = 30.0
SS_DEFAULT_THICKNESS = 2

class SSImage(object):
  def __init__(self, fname):
    super(SSImage, self).__init__()
    self.fname = fname
    self.image = cv2.imread(fname, cv2.IMREAD_UNCHANGED)

  def size(self):
    shape = self.image.shape
    #注意shape里面的值是高x宽xchannel
    return (shape[1], shape[0])

  def date(self):
    image = Image.open(self.fname)
    exif = image._getexif()
    if exif and len(exif) > 36868:
      return (str)(exif[36867])
    else:
      print(self.fname + " no timeStamp")
      return None

  def rawImage(self):
    return self.image
    
  def addTimestamp(self, timeStamp):
    text = self.date()
    if text:
      timeStamp.fitSize(self.size(), self.date())
      timeStamp.drawOnImage(self.image)

  def save(self):
    cv2.imwrite(self.fname, self.image)

class SSTimestamp(object):
  def __init__(self):
    self.font = cv2.FONT_HERSHEY_SIMPLEX
    self.color = (0, 0, 0) #bgr

  #size: (width, height)
  def fitSize(self, size, text):
    self.text = text

    imageHeight = size[1]
    imageWidth = size[0]
    desiredFontHeight = imageHeight / SS_DEFAULT_SCALE

    fontScale = 1
    textSize = cv2.getTextSize(text, self.font, fontScale, SS_DEFAULT_THICKNESS)
    textHeight = textSize[0][1]

    self.fontScale = (int)(desiredFontHeight / textHeight)
    self.thickness = SS_DEFAULT_THICKNESS * self.fontScale

    textSize = cv2.getTextSize(text, self.font, self.fontScale, self.thickness)
    textWidth = textSize[0][0]

    #right margin = bottom margin = desiredFontHeight
    self.position = ((int)(imageWidth - textWidth - desiredFontHeight), (int)(imageHeight - desiredFontHeight))

  def drawOnImage(self, image):
    cv2.putText(image, self.text, self.position, self.font, self.fontScale, self.color, self.thickness ,cv2.LINE_AA)

testImage = SSImage('1.jpg')
timeStamp = SSTimestamp()
testImage.addTimestamp(timeStamp)
result = testImage.rawImage()
testImage.save()

showImage = result[:,:,::-1]

plt.imshow(showImage)
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()
