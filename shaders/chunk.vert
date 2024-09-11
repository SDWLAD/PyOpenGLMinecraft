#version 330 core

layout (location = 0) in ivec3 in_position;
layout (location = 1) in int block_id;
layout (location = 2) in int face_id;
layout (location = 3) in int ao_id;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

out vec2 uv;
out float shading_color;

flat out int f_block_id;
flat out int f_face_id;

const float ao_values[4] = float[4](0.3, 0.5, 0.75, 1.0);

const vec2 uv_coords[4] = vec2[4](vec2(0, 0), vec2(0, 1),  vec2(1, 0), vec2(1, 1));
const int uv_indices[12] = int[12](1, 0, 2, 1, 2, 3, 3, 0, 2, 3, 1, 0);
const float face_shading[6] = float[6](1.0, 0.5, 0.5, 0.8, 0.5, 0.8);

void main() {
    f_block_id = block_id;
    f_face_id = face_id;
    uv = uv_coords[uv_indices[gl_VertexID % 6  + (face_id & 1) * 6]];
    shading_color = face_shading[face_id] * ao_values[ao_id];
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}