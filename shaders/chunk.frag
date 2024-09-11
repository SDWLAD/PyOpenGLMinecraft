#version 330 core

layout (location = 0) out vec4 fragColor;

uniform sampler2D texture_array_0;

in vec2 uv;
in float shading_color;

flat in int f_block_id;
flat in int f_face_id;

void main() {
    vec3 biome_col = vec3(1);

    vec2 face_uv = uv;
    face_uv.x = uv.x / 16.0 + (1.0-f_block_id/16.0);
    face_uv.y = uv.y / 16.0;

    if (f_block_id == 4 && f_face_id==0){
        face_uv.x = uv.x / 16.0 + (1.0-1.0/16.0);
        biome_col *= vec3(0.0, 0.8, 0.2);
    }

    vec3 tex_col = texture(texture_array_0, face_uv).rgb*shading_color*biome_col;
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
    tex_col = mix(tex_col, vec3(0.16, 0.27, 1), (1.0 - exp2(-0.0005 * fog_dist * fog_dist)));
    fragColor = vec4(tex_col, 1);
}