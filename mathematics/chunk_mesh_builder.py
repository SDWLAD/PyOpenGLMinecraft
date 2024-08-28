from settings import *
from numba import njit, uint8
import numpy as np

@njit(fastmath=True)
def to_uint8(x, y, z, voxel_id, face_id):
    return uint8(x), uint8(y), uint8(z), uint8(voxel_id), uint8(face_id)

@njit(fastmath=True)
def is_void(block_pos, chunk_blocks, chunk_position, chunks):
    x, y, z = block_pos
    cx, cy, cz = chunk_position
    if 0 <= x < CHUNK_WIDTH and 0 <= z < CHUNK_WIDTH:
        if chunk_blocks[x + CHUNK_WIDTH * z + CHUNK_WIDTH * CHUNK_WIDTH * y]:
            return False
        return True
    if x < 0: return is_void((CHUNK_WIDTH + x, y, z), chunks[0], chunk_position, chunks)
    if x >= CHUNK_WIDTH: return is_void((x - CHUNK_WIDTH, y, z), chunks[1], chunk_position, chunks)
    if z < 0: return is_void((x, y, CHUNK_WIDTH + z), chunks[2], chunk_position, chunks)
    if z >= CHUNK_WIDTH: return is_void((x, y, z - CHUNK_WIDTH), chunks[3], chunk_position, chunks)
    return True

@njit(fastmath=True)
def add_data(vertex_data, index, *vertices):
    for vertex in vertices:
        vertex_data[index:index+len(vertex)] = vertex
        index += len(vertex)
    return index

@njit(fastmath=True)
def build_chunk_mesh(chunk_blocks, format_size, chunk_position, chunks):
    vertex_data = np.empty((CHUNK_WIDTH*CHUNK_WIDTH*CHUNK_HEIGHT * 18 * format_size,), dtype=np.uint8)
    index = 0

    for x in range(CHUNK_WIDTH):
        for y in range(CHUNK_HEIGHT):
            for z in range(CHUNK_WIDTH):

                block_id = chunk_blocks[x + CHUNK_WIDTH * z + CHUNK_WIDTH * CHUNK_WIDTH * y]

                if not block_id:
                    continue

                if is_void((x, y + 1, z), chunk_blocks, chunk_position, chunks):
                    v0 = to_uint8(x, y + 1, z, block_id, 0)
                    v1 = to_uint8(x + 1, y + 1, z, block_id, 0)
                    v2 = to_uint8(x + 1, y + 1, z + 1, block_id, 0)
                    v3 = to_uint8(x, y + 1, z + 1, block_id, 0)
                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                if is_void((x, y - 1, z), chunk_blocks, chunk_position, chunks) and y != 0:
                    v0 = to_uint8(x, y, z, block_id, 1)
                    v1 = to_uint8(x + 1, y, z, block_id, 1)
                    v2 = to_uint8(x + 1, y, z + 1, block_id, 1)
                    v3 = to_uint8(x, y, z + 1, block_id, 1)
                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                if is_void((x + 1, y, z), chunk_blocks, chunk_position, chunks):
                    v0 = to_uint8(x + 1, y, z, block_id, 2)
                    v1 = to_uint8(x + 1, y + 1, z, block_id, 2)
                    v2 = to_uint8(x + 1, y + 1, z + 1, block_id, 2)
                    v3 = to_uint8(x + 1, y, z + 1, block_id, 2)
                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                if is_void((x - 1, y, z), chunk_blocks, chunk_position, chunks):
                    v0 = to_uint8(x, y, z, block_id, 3)
                    v1 = to_uint8(x, y + 1, z, block_id, 3)
                    v2 = to_uint8(x, y + 1, z + 1, block_id, 3)
                    v3 = to_uint8(x, y, z + 1, block_id, 3)
                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                if is_void((x, y, z - 1), chunk_blocks, chunk_position, chunks):
                    v0 = to_uint8(x, y, z, block_id, 4)
                    v1 = to_uint8(x, y + 1, z, block_id, 4)
                    v2 = to_uint8(x + 1, y + 1, z, block_id, 4)
                    v3 = to_uint8(x + 1, y, z, block_id, 4)
                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                if is_void((x, y, z + 1), chunk_blocks, chunk_position, chunks):
                    v0 = to_uint8(x, y, z + 1, block_id, 5)
                    v1 = to_uint8(x, y + 1, z + 1, block_id, 5)
                    v2 = to_uint8(x + 1, y + 1, z + 1, block_id, 5)
                    v3 = to_uint8(x + 1, y, z + 1, block_id, 5)
                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    return vertex_data[:index]

