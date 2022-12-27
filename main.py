import time

import pygame
from pygame.locals import RESIZABLE

import skills
from connection import Connection
from common_files.protocol import Protocol
from settings import Settings


class Server:
    def __init__(self):
        self.pressed_keys = list()
        self.sock_conn = Connection()
        self.protocol = Protocol(skills.skill_dict)
        self.sc = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT), RESIZABLE)
        self._clear_screen()
        pygame.display.set_caption("Robot Server V0.1")
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 72)
        self.is_working = True

    def run(self):
        self.sock_conn.connect(Settings.HOST, Settings.PORT)
        prev_packet = ""
        while self.is_working:
            self.clock.tick(Settings.WINDOW_FPS)
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    self._exit()
                    break
                elif i.type == pygame.KEYDOWN:
                    self.pressed_keys.append(i.key)
                elif i.type == pygame.KEYUP:
                    self.pressed_keys.remove(i.key)
            result = list()
            for skill_tag, skill in skills.skill_dict.items():
                skill_obj = skill()
                result.append(skill_obj.run(keys=self.pressed_keys))
            if result:
                current_packet = self.protocol.prepare_packet(data=result)
                if current_packet != prev_packet:
                    self._show_text(f"{time.time()} | {self.protocol.prepare_packet(data=result)}")
                    self.sock_conn.send(self.protocol.prepare_packet(data=result))
                    prev_packet = current_packet

    def _exit(self):
        self.sock_conn.close()
        pygame.quit()
        self.is_working = False

    def _clear_screen(self):
        self.sc.fill((255, 255, 255))
        pygame.display.update()

    def _key_pressed(self, key):
        self._clear_screen()
        if key == pygame.K_UP:
            txt = "UP pressed"

        else:
            txt = f"{key} pressed"
        self._show_text(txt)

    def _key_released(self, key):
        self._clear_screen()
        if key == pygame.K_UP:
            txt = "UP released"
        else:
            txt = f"{key} released"
        self._show_text(txt)

    def _show_text(self, text):
        self._clear_screen()
        text1 = self.font.render(text, True, (0, 0, 0))
        self.sc.blit(text1, (10, 50))
        pygame.display.update()


if __name__ == "__main__":
    server = Server()
    server.run()
