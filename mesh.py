from mathematics.chunk_mesh_builder import build_chunk_mesh
import numpy as np

import moderngl as mgl  
from settings import *

class Mesh():
    '''Стандартний клас для мешу'''
    def __init__(self, app, chunk):
        super().__init__()

        self.app = app
        self.chunk = chunk
        self.ctx:mgl.Context = app.ctx
        self.program = app.shader_program.chunk

        self.vbo_format = '3u1 1u1 1u1 1u1'
        self.attrs = ('in_position', 'block', 'face_id', 'ao_id')
        self.vertices = []
        self.triangles = []
        self.vao:mgl.VertexArray

    def rebuild(self):
        self.vao = self.get_vao()

    def get_vertex_data(self):
        mesh = build_chunk_mesh(
            chunk_blocks=self.chunk.blocks,
            format_size=sum(int(fmt[:1]) for fmt in self.vbo_format.split()),
            chunks=[self.chunk.side_chunks[0].blocks, self.chunk.side_chunks[1].blocks, self.chunk.side_chunks[2].blocks, self.chunk.side_chunks[3].blocks],
        )
        return mesh

    def get_vao(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        vao = self.ctx.vertex_array(
            self.program, [(vbo, self.vbo_format, *self.attrs)], skip_errors=True
        )
        return vao

    def render(self):
        self.vao.render()