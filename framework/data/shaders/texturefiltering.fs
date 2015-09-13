#version 330

im vec3 viewPortResolution; //viewport resoltuion
in float textureResolution; //texture resolution
in sampler2D texture; // 2D texture
in vec2 fragCoords; // Coordinates of the pixel

out vec4 outputColor; // Final color

vec4 imageFilter(in vec2 fragCoord)
{
	vec2 p = fragCoord.xy / viewPortResolution.xy;
	vec2 uv = p * 1.0; // This is to scale the texture (1.0 being original size)

	uv = uv * textureResolution + 0.5;

	vec2 iuv = floor(uv);
	vec2 fuv = fract(uv);

	uv = iuv + fuv*fuv * (3.0 - 2.0 * fuv); // fuv * fuv * fuv * (fuv * (fuv * 6.0 - 15.0) + 10.0);

	uv = (uv - 0.5) / textureResolution;

	vec3 color = texture2D(texture, uv).xyz;

	vec4 fragColor = vec4(color, 1.0);

	return fragColor;
}

void main()
{
	outputColor = imageFilter(fragCoords);
}