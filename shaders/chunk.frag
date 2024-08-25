#version 330 core

layout (location = 0) out vec4 fragColor;

uniform sampler2D u_texture_0;

in vec2 uv;
in float shading_color;

void main() {
    vec3 tex_col = texture(u_texture_0, uv).rgb*shading_color;
    fragColor = vec4(tex_col, 1);
}