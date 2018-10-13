import pycuda.autoinit
from pycuda.compiler import SourceModule

gpu_mandelbrot_string = """
    __global__ void mandelbrot(float* real, float* imag, int* iter, int maxIterations, int bailout2, int width, int height){
        int xCoord = blockDim.x * blockIdx.x + threadIdx.x;
        int yCoord = blockDim.y * blockIdx.y + threadIdx.y;
        if(xCoord < width && yCoord < height){
            float a = real[xCoord];
            float b = imag[yCoord];
            float zReal = 0.0;
            float zImag = 0.0;
            float zR2 = 0.0;
            float zI2 = 0.0;
            float temp = 0.0;
            int iterations;
            for(iterations = 0; iterations < maxIterations; iterations++){
                zR2 = zReal * zReal;
                zI2 = zImag * zImag;
                if(zR2 + zI2 > bailout2){
                    break;
                }
                temp = zR2 - zI2 + a;
                zImag = 2*zReal*zImag + b;
                zReal = temp;
            }
            iter[xCoord + yCoord*height] = iterations;
        }
    }
    """

gpu_mandelbrot = SourceModule(gpu_mandelbrot_string)
mandelbrotKernel = gpu_mandelbrot.get_function("mandelbrot")