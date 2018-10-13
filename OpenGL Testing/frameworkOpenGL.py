from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import os
import sys

def loadShader(shaderType, shaderFile):
    shaderData = None
    with open(shaderFile, 'r') as f:
        shaderData = f.read()

    shader = glCreateShader(shaderType)
    glShaderSource(shader, shaderData)

    glCompileShader(shader)

    status = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if status == GL_FALSE:
        strInfoLog = glGetShaderInfoLog(shader)
        strShaderType = ""
        if shaderType is GL_VERTEX_SHADER:
            strShaderType = "vertex"
        elif shaderType is GL_GEOMETRY_SHADER:
            strShaderType = "geometry"
        elif shaderType is GL_FRAGMENT_SHADER:
            strShaderType = "fragment"

        print("Compilation failure for " + strShaderType + " shader:\n" + strInfoLog.decode("utf-8"))
    return shader

def createProgram(shaderList):
    program = glCreateProgram()

    for shader in shaderList:
        glAttachShader(program, shader)

    glLinkProgram(program)

    status = glGetProgramiv(program, GL_LINK_STATUS)
    if status == GL_FALSE:
        strInfoLog = glGetProgramInfoLog(program)
        print("Linker failure: \n" + strInfoLog)

    for shader in shaderList:
        glDetachShader(program, shader)

    return program