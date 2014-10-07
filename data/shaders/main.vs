#version 330

layout(location = 0) in vec2 position;
layout(location = 1) in vec2 vertexUV;

out vec2 UV;

uniform mat4 ortho;

void main()
{
	gl_Position = ortho * vec4(position, 0.0, 1.0);
	UV = vertexUV;
}