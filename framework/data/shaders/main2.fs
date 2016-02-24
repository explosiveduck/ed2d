#version 330 core

// Interpolated values from the vertex shaders
in vec4 fragmentColor;

// Input interpolant from the vertex shader for the logarithmic depth buffer
in float logz;

// Ouput data
out vec4 color;

// Constant used in logarithmic depth buffer calculation
const float  Fcoef = 2.0 / log2(1e27 + 1.0);

void main(){

	// Output color = color specified in the vertex shader,
	// interpolated between all 3 surrounding vertices
	color = fragmentColor;

	// Writing the fragment depth because of issues with depth not being interpolated perspectively
	// This can cause issues with high overdraw.
	// This can be removed once adpative tesselation is available.
	// This could be split, tesselation for big objects or dynamic stuff, and static objects just use this.
	gl_FragDepth = log2(logz) * Fcoef * 0.5;

}
