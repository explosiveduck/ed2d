#version 330

in vec2 UV;

out vec4 outputColor;

uniform sampler2D textureSampler;

void main()
{

	outputColor = vec4(1.0, 1.0, 1.0, texture(textureSampler, UV ).r);
}