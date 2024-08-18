import pygame as pg
from camera import Camera
from settings import *


class Player(Camera):
    def __init__(self, app, position=glm.vec3(0, 10, 0)):
        super().__init__(position, -90, 0)
        self.game_cls = app

    def update(self):
        self.keyboard_control()
        self.mouse_control()
        super().update()

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx: self.rotation.x+=mouse_dx * MOUSE_SENSITIVITY
        if mouse_dy: self.rotation.y-=mouse_dy * MOUSE_SENSITIVITY

    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        if key_state[pg.K_w]: self.position += glm.normalize(glm.vec3(self.forward.x, 0, self.forward.z)) * PLAYER_SPEED
        if key_state[pg.K_s]: self.position -= glm.normalize(glm.vec3(self.forward.x, 0, self.forward.z)) * PLAYER_SPEED
        if key_state[pg.K_d]: self.position += self.right   * PLAYER_SPEED
        if key_state[pg.K_a]: self.position -= self.right   * PLAYER_SPEED
        if key_state[pg.K_SPACE]: self.position += self.up  * PLAYER_SPEED
        if key_state[pg.K_LSHIFT]: self.position -= self.up * PLAYER_SPEED