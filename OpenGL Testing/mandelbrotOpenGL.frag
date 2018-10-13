#version 410

uniform int maxIterations;
uniform double bailoutSqr;
uniform dvec4 range;
uniform vec2 dimensions;
uniform int texSize;
out vec4 outputColor;

uniform sampler2D colors;

void setColor(float iteration){
    ivec2 coord1 = ivec2(mod(floor(iteration), texSize), floor(iteration/texSize));
    ivec2 coord2 = ivec2(mod(ceil(iteration), texSize), floor((iteration+1)/texSize));
    vec4 color1 = texelFetch(colors, coord1, 0);
    vec4 color2 = texelFetch(colors, coord2, 0);
    outputColor = mix(color1, color2, iteration - floor(iteration));
}

void main()
{
	double xMin = range.x;
	double xMax = range.y;
	double yMin = range.z;
	double yMax = range.w;
	double cR = mix(xMin, xMax, gl_FragCoord.x / dimensions.x);
	double cI = mix(yMin, yMax, gl_FragCoord.y / dimensions.y);
	double zR = 0.0f;
	double zI = 0.0f;
	double temp = 0.0f;
	double zR2 = 0.0f;
	double zI2 = 0.0f;
	int iter = 0;
	while(zR2 + zI2 <= bailoutSqr && iter <= maxIterations){
	    iter += 1;
	    temp = zR2 - zI2 + cR;
	    zI = 2*zR*zI + cI;
	    zR = temp;
	    zR2 = zR*zR;
	    zI2 = zI*zI;
	}
	float newIter = float(maxIterations);
	if(iter < maxIterations){
	    float potential = log(float(zR2 + zI2)) / 2;
	    float frac = log(potential / log(2)) / log(2);
	    newIter = iter + 1 - frac;
	}
	setColor(newIter);
}