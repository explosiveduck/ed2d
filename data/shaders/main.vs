#version 330

layout(location = 0) in vec2 position;

uniform mat4 ortho;

void main()
{
	gl_Position = ortho * vec4(position, 0.0, 1.0);
}