#version 330
in vec3 fragColor;
in vec2 UV;

uniform sampler2D textureSampler;
uniform vec2 viewPortResolution;
uniform vec2 textureResolution;

out vec4 outputColor;


vec4 imageFilter(vec2 test)
{
	
	vec2 uv = test.xy * textureResolution * 1.0 + 0.5;

	vec2 iuv = floor(uv);
	vec2 fuv = fract(uv);

	uv = iuv + fuv*fuv * (3.0 - 2.0 * fuv); // fuv * fuv * fuv * (fuv * (fuv * 6.0 - 15.0) + 10.0);

	uv = (uv - 0.5) / textureResolution;

	vec3 color = texture(textureSampler, uv).xyz;
	
	vec4 fragColor = vec4(color, 1.0);

	return fragColor;
}

void main()
{
	outputColor = vec4(fragColor, 1.0) + imageFilter(UV);
}