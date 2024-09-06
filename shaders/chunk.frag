#version 330 core

layout (location = 0) out vec4 fragColor;

uniform sampler2DArray texture_array_0;

in vec2 uv;
in float shading_color;
flat in int face_id;

void main() {
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;


    vec3 tex_col = texture(texture_array_0, vec3(face_uv, 1)).rgb*shading_color;
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
    tex_col = mix(tex_col, vec3(0.16, 0.27, 1), (1.0 - exp2(-0.0005 * fog_dist * fog_dist)));
    fragColor = vec4(tex_col, 1);
}