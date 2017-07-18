#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# timestamp dir //遍历dir中的所有图片, 添加时间戳
# timestamp file //给file添加时间戳

import os, sys, cv2
from matplotlib import pyplot as plt
from PIL import Image

SS_DEFAULT_SCALE = 30.0
SS_DEFAULT_THICKNESS = 2

class SSImage(object):
  def __init__(self, fname):
    super(SSImage, self).__init__()
    self.fname = fname
    self.image = cv2.imread(fname, cv2.IMREAD_UNCHANGED)
  
  def isValid(self):
    if self.image is None:
      return False
    else:
      return True

  def size(self):
    shape = self.image.shape
    #注意shape里面的值是高x宽xchannel
    return (shape[1], shape[0])

  def date(self):    
    try:
      image = Image.open(self.fname)
      exif = image._getexif()
      if exif:
        return (str)(exif[36867])
      else:
        print(self.fname + " no timeStamp")
        return None
    except:
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

def showImage(image):
  showImage = image[:,:,::-1]
  plt.imshow(showImage)
  plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
  plt.show()

def addTimestamp(file):
  image = SSImage(file)
  if image.isValid():
    stamp = SSTimestamp()
    image.addTimestamp(stamp)
    image.save()
    #showImage(image.rawImage())

def processDir(rootDir): 
  for lists in os.listdir(rootDir): 
    path = os.path.join(rootDir, lists) 
    print(path)
    addTimestamp(path)
    if os.path.isdir(path): 
      processDir(path) 

if len(sys.argv) >= 2:
  content = sys.argv[1]
  if os.path.isdir(content):
    processDir(content)
  else:
    addTimestamp(content)
else:
  print('usage: timestamp dir')
