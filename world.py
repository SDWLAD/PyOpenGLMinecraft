from settings import *
from world_objects.chunk import Chunk

class World:
    def __init__(self, game_cls):
        self.game_cls = game_cls
        self.chunks = {}
        self.chunks_stack = []

    def create_chunk(self, chunk, x, z):
        chunk.generate_chunk()
        chunk.side_chunks = [
            self.chunks.get((x + dx, z + dz), Chunk(self.game_cls)) for dx, dz in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        ]
        chunk.mesh.vao = chunk.mesh.get_vao()

    def update_stack(self):
        if not self.chunks_stack: return
        chunk = self.chunks_stack[0]
        self.create_chunk(chunk, *chunk.position)
        [self.create_chunk(chunk.side_chunks[i], *chunk.side_chunks[i].position) for i in range(4) if
            chunk.side_chunks[i].position != (float("inf"), float("inf"))]
        self.chunks_stack.remove(chunk)
            

    def build_chunks(self, tick):
        i, j = map(lambda x: int(x//CHUNK_WIDTH), (self.game_cls.player.position.x, self.game_cls.player.position.z))
        for x in range(i - RENDER_DISTANCE, RENDER_DISTANCE + i + 1):
            for z in range(j - RENDER_DISTANCE, RENDER_DISTANCE + j + 1):
                if (x, z) not in self.chunks:
                    chunk = Chunk(self.game_cls, (x, z))
                    self.chunks[chunk.position] = chunk
                    if tick == 0:
                        self.create_chunk(chunk, *chunk.position)
                        [self.create_chunk(chunk.side_chunks[i], *chunk.side_chunks[i].position) for i in range(4) if
                            chunk.side_chunks[i].position != (float("inf"), float("inf"))]
                        continue
                    self.chunks_stack.append(chunk)

    def update(self, tick):
        self.build_chunks(tick)
        self.update_stack()

    def render(self):
        player_pos = self.game_cls.player.position
        player_chunk_pos = (int(player_pos.x // CHUNK_WIDTH), int(player_pos.z // CHUNK_WIDTH))
        render_range = range(-RENDER_DISTANCE, RENDER_DISTANCE + 1)

        for chunk_pos, chunk in self.chunks.items():
            if (chunk_pos[0] - player_chunk_pos[0] in render_range) and (chunk_pos[1] - player_chunk_pos[1] in render_range):
                try: chunk.render()
                except:...  
