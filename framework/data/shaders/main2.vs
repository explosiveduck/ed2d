#version 330 core

// Input vertex data, different for all executions of this shader.
layout(location = 0) in vec3 vertexPosition_modelspace;
layout(location = 1) in vec3 vertexColor;
layout(location = 2) in vec3 normal_modelspace;

// Output data ; will be interpolated for each fragment.
out vec4 fragmentColor;

// Output the interpolant to the pixel shader
out float logz;

// Values that stay constant for the whole mesh.
uniform mat4 view;
uniform mat4 persp;
uniform mat4 model_matrix;
uniform mat3 gMdVw;

// SPH Constants
const float C1 = 0.429043;
const float C2 = 0.511664;
const float C3 = 0.743125;
const float C4 = 0.886227;
const float C5 = 0.247708;

// Constants for Old Town Square lighting
const vec3 L00  = vec3( 0.871297,  0.875222,  0.864470);
const vec3 L1m1 = vec3( 0.175058,  0.245335,  0.312891);
const vec3 L10  = vec3( 0.034675,  0.036107,  0.037362);
const vec3 L11  = vec3(-0.004629, -0.029448, -0.048028);
const vec3 L2m2 = vec3(-0.120535, -0.121160, -0.117507);
const vec3 L2m1 = vec3( 0.003242,  0.003624,  0.007511);
const vec3 L20  = vec3(-0.028667, -0.024926, -0.020998);
const vec3 L21  = vec3(-0.077539, -0.086325, -0.091591);
const vec3 L22  = vec3(-0.161784, -0.191783, -0.219152);

// Constant used in logarithmic depth buffer calculation
const float  Fcoef = 2.0 / log2(1e27 + 1.0);

// Local Variables
vec3 vertNormal;

void main(){

	// Output position of the vertex, in clip space : MVP * position
	gl_Position =  persp * view * model_matrix * vec4(vertexPosition_modelspace,1);

	// Output normal of the vertex: Transpose Inverse Model Matrix * normal
	vertNormal = gMdVw * normal_modelspace;

	// logarithmic Depth equation (optimized)
	gl_Position.z = (log2(max(1e-7, 1.0 + gl_Position.w)) * Fcoef - 1.0);

	// Interpolant for the logarithmic depth buffer, used in the pixel shader
	logz = 1.0 + gl_Position.w;

	fragmentColor =  vec4(C1 * L22 * (vertNormal.x * vertNormal.x - vertNormal.y * vertNormal.y) +
								C3 * L20 * vertNormal.z * vertNormal.z +
								C4 * L00 -
								C5 * L20 +
								2.0 * C1 * L2m2 * vertNormal.x * vertNormal.y +
								2.0 * C1 * L21  * vertNormal.x * vertNormal.z +
								2.0 * C1 * L2m1 * vertNormal.y * vertNormal.z +
								2.0 * C2 * L11  * vertNormal.x +
								2.0 * C2 * L1m1 * vertNormal.y +
								2.0 * C2 * L10  * vertNormal.z, 1.0);

	fragmentColor *= 0.9;
	
	// The color of each vertex will be interpolated
	// to produce the color of each fragment
	fragmentColor *= vec4(vertexColor,1.0);
}
