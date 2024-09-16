from settings import *
from mesh import *

from block.BlockAir import BlockAir
from block.BlockStone import BlockStone
from block.BlockDirt import BlockDirt
from block.BlockGrass import BlockGrass

class Chunk:
    def __init__(self, game, position=(float("inf"), float("inf"))):
        self.position = position
        self.blocks = np.zeros(CHUNK_WIDTH * CHUNK_HEIGHT * CHUNK_WIDTH)
        self.mesh = Mesh(game, self)
        self.m_model = self.get_model_matrix()
        self.side_chunks=[None, None, None, None]
        
    def generate_chunk(self):
        for x in range(CHUNK_WIDTH):
            for z in range(CHUNK_WIDTH):
                world_height = int(glm.simplex(glm.vec2(x+self.position[0]*CHUNK_WIDTH, z+self.position[1]*CHUNK_WIDTH) * 0.01) * 32 + 32)
                for y in range(world_height):
                    if y == world_height-1: block = BlockGrass()
                    elif y >= world_height-4: block = BlockDirt()
                    else: block = BlockStone()

                    if world_height < 6: block = BlockStone()

                    self.blocks[x + CHUNK_WIDTH * z + CHUNK_WIDTH*CHUNK_WIDTH * y] = block.id

    def get_model_matrix(self):
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position[0], 0, self.position[1]) * CHUNK_WIDTH)
        return m_model

    def set_uniform(self):
        self.mesh.program['m_model'].write(self.m_model)

    def render(self):
        self.set_uniform()
        self.mesh.render()
    
    def __repr__(self):
        return str(self.position)