from settings import *
from numba import njit, uint8
import numpy as np

@njit
def get_ao(local_pos, chunk_blocks, chunks, plane):
    x, y, z = local_pos

    if plane == 'Y':
        a = is_void((x    , y, z - 1), chunk_blocks, chunks)
        b = is_void((x - 1, y, z - 1), chunk_blocks, chunks)
        c = is_void((x - 1, y, z    ), chunk_blocks, chunks)
        d = is_void((x - 1, y, z + 1), chunk_blocks, chunks)
        e = is_void((x    , y, z + 1), chunk_blocks, chunks)
        f = is_void((x + 1, y, z + 1), chunk_blocks, chunks)
        g = is_void((x + 1, y, z    ), chunk_blocks, chunks)
        h = is_void((x + 1, y, z - 1), chunk_blocks, chunks)

    elif plane == 'X':
        a = is_void((x, y    , z - 1), chunk_blocks, chunks)
        b = is_void((x, y - 1, z - 1), chunk_blocks, chunks)
        c = is_void((x, y - 1, z    ), chunk_blocks, chunks)
        d = is_void((x, y - 1, z + 1), chunk_blocks, chunks)
        e = is_void((x, y    , z + 1), chunk_blocks, chunks)
        f = is_void((x, y + 1, z + 1), chunk_blocks, chunks)
        g = is_void((x, y + 1, z    ), chunk_blocks, chunks)
        h = is_void((x, y + 1, z - 1), chunk_blocks, chunks)

    else:  # Z plane
        a = is_void((x - 1, y    , z), chunk_blocks, chunks)
        b = is_void((x - 1, y - 1, z), chunk_blocks, chunks)
        c = is_void((x    , y - 1, z), chunk_blocks, chunks)
        d = is_void((x + 1, y - 1, z), chunk_blocks, chunks)
        e = is_void((x + 1, y    , z), chunk_blocks, chunks)
        f = is_void((x + 1, y + 1, z), chunk_blocks, chunks)
        g = is_void((x    , y + 1, z), chunk_blocks, chunks)
        h = is_void((x - 1, y + 1, z), chunk_blocks, chunks)

    ao = (a + b + c), (g + h + a), (e + f + g), (c + d + e)
    return ao

@njit(fastmath=True)
def to_uint8(x, y, z, voxel_id, face_id, ao_id):
    return uint8(x), uint8(y), uint8(z), uint8(voxel_id), uint8(face_id), uint8(ao_id)

@njit(fastmath=True)
def is_void(block_pos, chunk_blocks, chunks):
    x, y, z = block_pos
    if 0 <= x < CHUNK_WIDTH and 0 <= z < CHUNK_WIDTH:
        if chunk_blocks[x + CHUNK_WIDTH * z + CHUNK_WIDTH * CHUNK_WIDTH * y]:
            return False
        return True
    if x < 0: return is_void((CHUNK_WIDTH + x, y, z), chunks[0], chunks)
    if x >= CHUNK_WIDTH: return is_void((x - CHUNK_WIDTH, y, z), chunks[1], chunks)
    if z < 0: return is_void((x, y, CHUNK_WIDTH + z), chunks[2], chunks)
    if z >= CHUNK_WIDTH: return is_void((x, y, z - CHUNK_WIDTH), chunks[3], chunks)
    return True

@njit(fastmath=True)
def add_data(vertex_data, index, *vertices):
    for vertex in vertices:
        vertex_data[index:index+len(vertex)] = vertex
        index += len(vertex)
    return index

@njit(fastmath=True)
def build_chunk_mesh(chunk_blocks, format_size, chunks):
    vertex_data = np.empty((CHUNK_WIDTH*CHUNK_WIDTH*CHUNK_HEIGHT * 18 * format_size,), dtype=np.uint8)
    index = 0

    for x in range(CHUNK_WIDTH):
        for y in range(CHUNK_HEIGHT):
            for z in range(CHUNK_WIDTH):

                block_id = chunk_blocks[x + CHUNK_WIDTH * z + CHUNK_WIDTH * CHUNK_WIDTH * y]

                if not block_id:
                    continue

                if is_void((x, y + 1, z), chunk_blocks, chunks):
                    ao = get_ao((x, y + 1, z), chunk_blocks, chunks, plane='Y')

                    v0 = to_uint8(x, y + 1, z, block_id, 0, ao[0])
                    v1 = to_uint8(x + 1, y + 1, z, block_id, 0, ao[1])
                    v2 = to_uint8(x + 1, y + 1, z + 1, block_id, 0, ao[2])
                    v3 = to_uint8(x, y + 1, z + 1, block_id, 0, ao[3])
                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                if is_void((x, y - 1, z), chunk_blocks, chunks) and y != 0:
                    ao = get_ao((x, y - 1, z), chunk_blocks, chunks, plane='Y')

                    v0 = to_uint8(x, y, z, block_id, 1, ao[0])
                    v1 = to_uint8(x + 1, y, z, block_id, 1, ao[1])
                    v2 = to_uint8(x + 1, y, z + 1, block_id, 1, ao[2])
                    v3 = to_uint8(x, y, z + 1, block_id, 1, ao[3])
                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                if is_void((x + 1, y, z), chunk_blocks, chunks):
                    ao = get_ao((x + 1, y, z), chunk_blocks, chunks, plane='X')

                    v0 = to_uint8(x + 1, y, z, block_id, 2, ao[0])
                    v1 = to_uint8(x + 1, y + 1, z, block_id, 2, ao[1])
                    v2 = to_uint8(x + 1, y + 1, z + 1, block_id, 2, ao[2])
                    v3 = to_uint8(x + 1, y, z + 1, block_id, 2, ao[3])
                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                if is_void((x - 1, y, z), chunk_blocks, chunks):
                    ao = get_ao((x - 1, y, z), chunk_blocks, chunks, plane='X')

                    v0 = to_uint8(x, y, z, block_id, 3, ao[0])
                    v1 = to_uint8(x, y + 1, z, block_id, 3, ao[1])
                    v2 = to_uint8(x, y + 1, z + 1, block_id, 3, ao[2])
                    v3 = to_uint8(x, y, z + 1, block_id, 3, ao[3])
                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                if is_void((x, y, z - 1), chunk_blocks, chunks):
                    ao = get_ao((x, y, z - 1), chunk_blocks, chunks, plane='Z')

                    v0 = to_uint8(x, y, z, block_id, 4, ao[0])
                    v1 = to_uint8(x, y + 1, z, block_id, 4, ao[1])
                    v2 = to_uint8(x + 1, y + 1, z, block_id, 4, ao[2])
                    v3 = to_uint8(x + 1, y, z, block_id, 4, ao[3])
                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                if is_void((x, y, z + 1), chunk_blocks, chunks):
                    ao = get_ao((x, y, z + 1), chunk_blocks, chunks, plane='Z')

                    v0 = to_uint8(x, y, z + 1, block_id, 5, ao[0])
                    v1 = to_uint8(x, y + 1, z + 1, block_id, 5, ao[1])
                    v2 = to_uint8(x + 1, y + 1, z + 1, block_id, 5, ao[2])
                    v3 = to_uint8(x + 1, y, z + 1, block_id, 5, ao[3])
                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    return vertex_data[:index]

