from settings import *


class VoxelHandler:
    def __init__(self, world):
        self.app = world.app
        self.chunks = world.chunks

        # ray casting result
        self.chunk = None
        self.voxel_id = None
        self.voxel_index = None
        self.voxel_local_pos = None
        self.voxel_world_pos = None
        self.voxel_normal = None
    
    def add_voxel(self):
        pass

    def remove_voxel(self):
        if self.voxel_id:
            self.chunk.blocks[self.voxel_index] = 0

            self.chunk.mesh.rebuild()
            for i in range(4):
                if self.chunk.side_chunks[i]:
                    self.chunk.side_chunks[i].mesh.rebuild()
            

    def update(self):
        self.ray_cast()

    def ray_cast(self):
        x1, y1, z1 = self.app.player.position
        x2, y2, z2 = self.app.player.position + self.app.player.forward * MAX_RAY_DIST

        current_voxel_pos = glm.ivec3(glm.floor(x1), glm.floor(y1), glm.floor(z1))
        self.voxel_id = 0
        self.voxel_normal = glm.ivec3(0)
        step_dir = -1

        dx = glm.sign(x2 - x1)
        delta_x = abs(1.0 / (x2 - x1)) if dx != 0 else 10000000.0
        max_x = delta_x * (1.0 - glm.fract(x1)) if dx > 0 else delta_x * glm.fract(x1)

        dy = glm.sign(y2 - y1)
        delta_y = abs(1.0 / (y2 - y1)) if dy != 0 else 10000000.0
        max_y = delta_y * (1.0 - glm.fract(y1)) if dy > 0 else delta_y * glm.fract(y1)

        dz = glm.sign(z2 - z1)
        delta_z = abs(1.0 / (z2 - z1)) if dz != 0 else 10000000.0
        max_z = delta_z * (1.0 - glm.fract(z1)) if dz > 0 else delta_z * glm.fract(z1)

        while not (max_x > 1.0 and max_y > 1.0 and max_z > 1.0):
            result = self.get_voxel_id(voxel_world_pos=current_voxel_pos)
            if result[0]:
                self.voxel_id, self.voxel_index, self.voxel_local_pos, self.chunk = result
                self.voxel_world_pos = current_voxel_pos

                if step_dir == 0:
                    self.voxel_normal.x = -dx
                elif step_dir == 1:
                    self.voxel_normal.y = -dy
                else:
                    self.voxel_normal.z = -dz
                return True

            if max_x < max_y:
                if max_x < max_z:
                    current_voxel_pos.x += dx
                    max_x += delta_x
                    step_dir = 0
                else:
                    current_voxel_pos.z += dz
                    max_z += delta_z
                    step_dir = 2
            else:
                if max_y < max_z:
                    current_voxel_pos.y += dy
                    max_y += delta_y
                    step_dir = 1
                else:
                    current_voxel_pos.z += dz
                    max_z += delta_z
                    step_dir = 2
        return False
    
    def get_voxel_id(self, voxel_world_pos):
        cx, cy, cz = chunk_pos = glm.ivec3(
            math.floor(voxel_world_pos[0] / CHUNK_WIDTH),
            math.floor(voxel_world_pos[1] / CHUNK_HEIGHT),
            math.floor(voxel_world_pos[2] / CHUNK_WIDTH)
        )
        chunk = self.chunks[(cx, cz)]
        lx, ly, lz = voxel_local_pos = voxel_world_pos - chunk_pos * (CHUNK_WIDTH, CHUNK_HEIGHT, CHUNK_WIDTH)

        voxel_index = lx + CHUNK_WIDTH * lz + CHUNK_WIDTH*CHUNK_WIDTH * ly
        voxel_id = chunk.blocks[voxel_index]

        return voxel_id, voxel_index, voxel_local_pos, chunk
