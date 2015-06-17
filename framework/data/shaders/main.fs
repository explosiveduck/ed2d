#version 330

in vec2 UV;
in vec3 fragColor;

out vec4 outputColor;

uniform sampler2D textureSampler;

void main()
{
	outputColor = vec4(fragColor, 1.0) + texture(textureSampler, UV );
}