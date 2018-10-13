from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from array import array
import os
import sys
import numpy as np
from frameworkOpenGL import *
from textureGenerator import *
from math import sqrt, ceil

class Mandelbrot:

    def __init__(self, maxIter, bailoutRadius, center, distanceToClosestEdge, dimensions):
        self.maxIterations = maxIter
        self.bailoutSqr = bailoutRadius ** 2
        self.center = center #2-tuple
        self.distanceToClosestEdge = distanceToClosestEdge
        self.distanceToFurthestEdge = None
        self.dimensions = None #2-tuple
        self.changeDimensions(dimensions)

        self.shaders = None
        self.vertexBuffer = None
        self.texture = None

        self.vertexPositions = np.array([-1.0, 1.0, 0.0, 0.0,
                           -1.0, -1.0, 0.0, 0.0,
                           1.0, 1.0, 0.0, 0.0,
                           -1.0, -1.0, 0.0, 0.0,
                           1.0, -1.0, 0.0, 0.0,
                           1.0, 1.0, 0.0, 0.0], dtype='float32')

        self.vertexDimension = 4
        self.numVertices = 6
        self.textureSize = None

        self.maxIterations_loc = None
        self.bailoutSqr_loc = None
        self.windowRange_loc = None
        self.dimensions_loc = None
        self.textureSize_loc = None

    def getCoord(self, pixelX, pixelY):
        xMin, xMax, yMin, yMax = self.genWindowRange()
        width, height = self.dimensions
        x = (xMax - xMin) * pixelX / width + xMin
        y = (yMax - yMin) * (height - pixelY) / height + yMin
        return (x, y)

    def changeDimensions(self, newDimensions):
        self.dimensions = newDimensions
        width, height = self.dimensions
        if width < height:
            self.distanceToFurthestEdge = self.distanceToClosestEdge * height / width
        else:
            self.distanceToFurthestEdge = self.distanceToClosestEdge * width / height

    def zoom(self, factor):
        self.distanceToClosestEdge *= factor
        self.changeDimensions(self.dimensions)

    def genWindowRange(self):
        width = self.dimensions[0]
        height = self.dimensions[1]
        windowRange = np.zeros(4, dtype='float64')
        if width < height:
            windowRange[0] = self.center[0] - self.distanceToClosestEdge
            windowRange[1] = self.center[0] + self.distanceToClosestEdge
            windowRange[2] = self.center[1] - self.distanceToFurthestEdge
            windowRange[3] = self.center[1] + self.distanceToFurthestEdge
        else:
            windowRange[0] = self.center[0] - self.distanceToFurthestEdge
            windowRange[1] = self.center[0] + self.distanceToFurthestEdge
            windowRange[2] = self.center[1] - self.distanceToClosestEdge
            windowRange[3] = self.center[1] + self.distanceToClosestEdge
        return windowRange

    def initializeProgram(self):
        shaderList = []

        shaderList.append(loadShader(GL_VERTEX_SHADER, "mandelbrotOpenGL.vert"))
        shaderList.append(loadShader(GL_FRAGMENT_SHADER, "mandelbrotOpenGL.frag"))

        self.shaders = createProgram(shaderList)

        for shader in shaderList:
            glDeleteShader(shader)

    def initializeVertexBuffer(self):
        self.vertexBuffer = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        glBufferData(  # PyOpenGL allows for the omission of the size parameter
            GL_ARRAY_BUFFER,
            self.vertexPositions,
            GL_STATIC_DRAW
        )
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def initializeUniformValues(self):
        self.maxIterations_loc = glGetUniformLocation(self.shaders, 'maxIterations')
        self.bailoutSqr_loc = glGetUniformLocation(self.shaders, 'bailoutSqr')
        self.windowRange_loc = glGetUniformLocation(self.shaders, 'range')
        self.dimensions_loc = glGetUniformLocation(self.shaders, 'dimensions')
        self.textureSize_loc = glGetUniformLocation(self.shaders, 'texSize')

    def initializeTexture(self):
        self.texture = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        mandelbrotPixelList.maxIterations = self.maxIterations
        data = mandelbrotPixelList.genArray()
        self.textureSize = ceil(sqrt(len(data)))
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.textureSize, self.textureSize, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
        glBindTexture(GL_TEXTURE_2D, 0)

    def init(self):
        self.initializeProgram()
        self.initializeVertexBuffer()
        self.initializeUniformValues()
        self.initializeTexture()
        glBindVertexArray(glGenVertexArrays(1))


mandel = Mandelbrot(255, 2, (0, 0), 2, (500, 500))

def display():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(mandel.shaders)

    xMin, xMax, yMin, yMax = mandel.genWindowRange()
    width, height = mandel.dimensions
    glUniform1i(mandel.maxIterations_loc, mandel.maxIterations)
    glUniform1d(mandel.bailoutSqr_loc, mandel.bailoutSqr)
    glUniform4d(mandel.windowRange_loc, xMin, xMax, yMin, yMax)
    glUniform2f(mandel.dimensions_loc, width, height)
    glUniform1i(mandel.textureSize_loc, mandel.textureSize)

    glBindBuffer(GL_ARRAY_BUFFER, mandel.vertexBuffer)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, mandel.vertexDimension, GL_FLOAT, GL_FALSE, 0, None)
    glBindTexture(GL_TEXTURE_2D, mandel.texture)

    glDrawArrays(GL_TRIANGLES, 0, mandel.numVertices)

    glDisableVertexAttribArray(0)
    glUseProgram(0)

    glutSwapBuffers()
    glutPostRedisplay()

def keyboard(key, x, y):
    if ord(key) == 27:  # ord() is needed to get the keycode
        glutLeaveMainLoop()
        return
    if ord(key) == 61: #plus key
        mandel.maxIterations += 100
    if ord(key) == 45: #minus key
        mandel.maxIterations -= 100

def reshape(w, h):
    glViewport(0, 0, w, h)
    mandel.changeDimensions((w, h))

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == 0:
        center = mandel.getCoord(x, y)
        mandel.center = center

def mouseWheel(button, dir, x, y):
    mandel.zoom(1 - dir * 0.05)


def main():
    glutInit()
    displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH | GLUT_STENCIL;
    glutInitDisplayMode(displayMode)

    width = mandel.dimensions[0]
    height = mandel.dimensions[1]
    glutInitWindowSize(width, height)

    glutInitWindowPosition(300, 200)

    window = glutCreateWindow("Mandelbrot Viewer")

    mandel.init()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMouseWheelFunc(mouseWheel)

    glutMainLoop();


if __name__ == '__main__':
    main()