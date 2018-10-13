import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule
from mandelbrotKernel import mandelbrotKernel

import numpy as np
import time
from tkinter import Tk, Canvas, PhotoImage, mainloop


def linearInterpolate(min, max, samples):
    res = np.zeros(samples)
    scale = (max - min)/len(res)
    for i in range(len(res)):
        res[i] = scale * i + min
    return res


class Color:

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b




class Mandelbrot:

    def __init__(self, width, height, center, zoom):
        self.width = width
        self.height = height
        self.center = center
        self.zoom = zoom
        self.xMin = -2.0
        self.xMax = 2.0
        self.yMin = -2.0
        self.yMax = 2.0

    def draw(self):
        return 1

WIDTH, HEIGHT = 1024, 1024
xMin = -2.0
xMax = 2.0
yMin = -2.0
yMax = 2.0
xCoords = linearInterpolate(xMin, xMax, WIDTH).astype(np.float32)
yCoords = linearInterpolate(yMin, yMax, HEIGHT).astype(np.float32)

block = (32, 32, 1)
grid = (32, 32, 1)
iterations = np.zeros(WIDTH*HEIGHT).astype(np.int32)
maxIter = np.int32(255)
bailout2 = np.int32(4)

prgmWidth = np.int32(WIDTH)
prgmHeight = np.int32(HEIGHT)


start_time =  time.time()
mandelbrotKernel(drv.In(xCoords), drv.In(yCoords), drv.Out(iterations), maxIter, bailout2, prgmWidth, prgmHeight, block=block, grid=grid)
print("--- %s seconds ---" % (time.time() - start_time))





window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#000000")
canvas.pack()
img = PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")

start_time =  time.time()
pixelString = ' '
for y in range(HEIGHT):
    line = '{'
    for x in range(WIDTH):
        iter = iterations[y * HEIGHT + x]
        line = line + " #%02x%02x%02x" % (iter, iter, iter)
    line = line + '}'
    pixelString = pixelString + line + ' '

img.put(pixelString)
print("--- %s seconds ---" % (time.time() - start_time))

mainloop()

