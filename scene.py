from settings import *
from world_objects.chunk import Chunk


class Scene:
    def __init__(self, app):
        self.app = app  
        self.chunk = Chunk(self.app, (0, 0))
        self.chunk.generate_chunk()
        self.chunk.mesh.vao = self.chunk.mesh.get_vao()

    def update(self):
        pass

    def render(self):
        self.chunk.render()