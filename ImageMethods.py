import os.path

from PIL import *
import numpy as np
from PIL import Image
from PIL import *



def readImage(path):
    print(type(path))
    image = Image.open(path)
    #image.show()
    image = image.convert('RGB')
    #self.image.show()
    #gray_image.show()
    return image

def color2gray(image):
    image_gray = image.convert('L')
    return image_gray

def imageToArray(image):
    row = image.size[0]
    column = image.size[1]
    #print(f"row: {row}, column {column}")
    #image.show()
    image_array = np.array(image) # What convert does in here? Check Later.
    #print(image_array[32][16])
    return image_array

def fixArray(array):
    n = len(array)
    m = len(array[0])
    darr = np.array(array, copy= True)

    for i in range(n):
        for j in range(1, m):
            darr[i][j] = array[i][j] + darr[i][j - 1]

    return darr

"""def ArrayToImage(image):
    newimage = Image.fromarray(np.uint8(image)) #np.uint8(image) ???
    newimage.save(path + '.png')
    newimage.show()
    return newimage"""

def npToPIL(width, height, decompressed): #Is this neccessary ??

    arr = np.array(decompressed)
    #arr = arr.flatten()
    #print(arr)
    #numb = max(height,width)

    arr = arr.reshape(height,width, 3)
    #arr = arr[:height, width, :]
    arr = fixArray(arr)
    image = Image.fromarray(np.uint8(arr))
    return image

