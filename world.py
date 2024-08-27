from settings import *
from world_objects.chunk import Chunk

class World:
    def __init__(self, app):
        self.app = app
        self.chunks = {}

    def create_chunk(self, chunk):
        """Generates and prepares a chunk for rendering."""
        chunk.generate_chunk()
        chunk.mesh.vao = chunk.mesh.get_vao()

    def build_chunks(self, tick):
        if tick % 10 == 0:
            player_x, player_z = map(lambda x: int(x // CHUNK_WIDTH), (self.app.player.position.x, self.app.player.position.z))
            for i in range(player_x-RENDER_DISTANCE, player_x+RENDER_DISTANCE + 1):
                for j in range(player_z-RENDER_DISTANCE, player_z+RENDER_DISTANCE + 1):
                    if (i, j) not in self.chunks:
                        self.chunks[(i, j)] = Chunk(self.app, (i, j))
                        self.create_chunk(self.chunks[(i, j)])

    def update(self, tick):
        self.build_chunks(tick)

    def render(self):
        """Renders only the chunks within the render distance of the player."""
        player_x, player_z = map(lambda x: int(x // CHUNK_WIDTH), (self.app.player.position.x, self.app.player.position.z))
        render_range_x = range(player_x - RENDER_DISTANCE, player_x + RENDER_DISTANCE + 1)
        render_range_z = range(player_z - RENDER_DISTANCE, player_z + RENDER_DISTANCE + 1)

        for i in render_range_x:
            for j in render_range_z:
                if (i, j) in self.chunks:
                    self.chunks[(i, j)].render()