import numpy as np

def interpolate(min, max, prop):
    return (max - min) * prop + min


class Color:

    def __init__(self, r, g, b, iteration):
        self.r = r
        self.g = g
        self.b = b
        self.iteration = iteration

    def __str__(self):
        return str(self.iteration) + " --- (" + str(self.r) + ", " + str(self.g) + ", " + str(self.b) + ")"

class ColorList:

    def __init__(self, maxIterations):
        self.colors = []
        self.maxIterations = maxIterations

    def __str__(self):
        string = ""
        for i in range(len(self.colors)):
            string += str(self.colors[i]) + "\n"
        return string

    def addColor(self, color):
        if len(self.colors) == 0:
            if not color.iteration == 0:
                raise ValueError('The first color in the colorList must have an iteration threshold of 0.')
        elif self.colors[-1].iteration >= color.iteration:
            raise ValueError("New colors added to the colorList must have an iteration threshold greater than previous values in the list.")
        self.colors.append(color)

    def genArray(self):
        arr = np.zeros((self.maxIterations+1) * 3, dtype='uint8')
        index = 0
        colorIndex = 0
        colorsLength = len(self.colors)
        while index < len(arr):
            this = self.colors[colorIndex % colorsLength]
            next = self.colors[(colorIndex+1) % colorsLength]
            colorIndex += 1
            numColors = next.iteration - this.iteration
            interColorIndex = 0
            while interColorIndex < numColors and index < len(arr):
                arr[index] = interpolate(this.r, next.r, interColorIndex/numColors)
                arr[index+1] = interpolate(this.g, next.g, interColorIndex/numColors)
                arr[index+2] = interpolate(this.b, next.b, interColorIndex/numColors)
                index += 3
                interColorIndex += 1
        return arr

'''

Comment on the function above:
After this array is generated, it forms the data necessary for a 2d texture onto the gpu memory. The problem is that this
texture must be a square whose dimensions are a power of 2, so the area is very large but is filled with mostly unused
space (Say we wont 2000 iterations, we would use the first 2000 of a 512x512 image but discard the rest). If we organize
the data in row major order just by starting from the beginning, then we would have to write a program to take us to
the proper coordinates by knowing the texture size itself so it can traverse the array. Instead, we would take the color
data and use it to form an image of a hilbert curve. Since a hilbert curve is a 1d mapping to 2d, then we can give it a
single input from 0 to 1 (say iter/maxIter) and output to a 2d coordinate on the texture image. For this to work, the color
corresponding with a given iteration would have to be surrounding the area where that iteration maps to on the hilbert 
curve. However, by doing this we have constructed a function that maps a single input to a texture coordinate without
knowing the width of the texture image. This could be an approach considered to making the texture for the color pallete.

'''

black = Color(0, 0, 0, 0)
blue = Color(16, 52, 166, 15)
white = Color(255, 255, 255, 31)
orange = Color(253, 106, 2, 47)
end = Color(0, 0, 0, 63)
mandelbrotPixelList = ColorList(0)
mandelbrotPixelList.addColor(black)
mandelbrotPixelList.addColor(blue)
mandelbrotPixelList.addColor(white)
mandelbrotPixelList.addColor(orange)
mandelbrotPixelList.addColor(end)

