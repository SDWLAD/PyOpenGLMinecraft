#version 330 core

layout (location = 0) in uint packed_data;

int x, y, z;
int block_id;
int face_id;
int ao_id;

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

void unpack(uint packed_data) {
    // a, b, c, d, e, f, g = x, y, z, voxel_id, face_id, ao_id, flip_id
    uint b_bit = 6u, c_bit = 6u, d_bit = 8u, e_bit = 3u, f_bit = 2u, g_bit = 1u;
    uint b_mask = 63u, c_mask = 63u, d_mask = 255u, e_mask = 7u, f_mask = 3u, g_mask = 1u;
    //
    uint fg_bit = f_bit + g_bit;
    uint efg_bit = e_bit + fg_bit;
    uint defg_bit = d_bit + efg_bit;
    uint cdefg_bit = c_bit + defg_bit;
    uint bcdefg_bit = b_bit + cdefg_bit;
    // unpacking vertex data
    x = int(packed_data >> bcdefg_bit);
    y = int((packed_data >> cdefg_bit) & b_mask);
    z = int((packed_data >> defg_bit) & c_mask);
    //
    block_id = int((packed_data >> efg_bit) & d_mask);
    face_id = int((packed_data >> fg_bit) & e_mask);
    ao_id = int((packed_data >> g_bit) & f_mask);
}

void main() {
    f_block_id = block_id;
    f_face_id = face_id;
    uv = uv_coords[uv_indices[gl_VertexID % 6  + (face_id & 1) * 6]];
    shading_color = face_shading[face_id] * ao_values[ao_id];
    gl_Position = m_proj * m_view * m_model * vec4(x, y, z, 1.0);
}