#version 330

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 vertexUV;
layout(location = 2) in vec3 color;

out vec2 UV;
out vec3 fragColor;

uniform mat4 ortho;
uniform mat4 model;

void main()
{
	gl_Position = ortho * model * vec4(position, 1.0);
	UV = vertexUV;
	fragColor = color;
}