import pygame
from pygame.locals import RESIZABLE

import skills
from common_files import Telemetry, Constants
from common_files.protocol import Protocol
from libs.redis_lib import RedisLib


class Server:
    def __init__(self):
        self.pressed_keys = list()
        self.broker = RedisLib(host=Constants.REDIS_HOST, port=Constants.REDIS_PORT)
        self.protocol = Protocol()
        self.telemetry = Telemetry()
        self._pygame_init()
        self.is_working = True

    def run(self):
        self.broker.connect()
        prev_packet = ""
        while self.is_working:
            self.clock.tick(Constants.WINDOW_FPS)
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
                self._show_text("|".join(self.telemetry.get_current_telemetry()), (10, 50))
                if current_packet != prev_packet:
                    self.broker.set(key=Constants.REDIS_CMD_KEY, value=self.protocol.prepare_packet(data=result))
                    prev_packet = current_packet
            list_of_params = self._get_actual_telemetry()
            if list_of_params:
                self._fill_telemetry(list_of_params)

    def _pygame_init(self):
        self.sc = pygame.display.set_mode((Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT), RESIZABLE)
        self._clear_screen()
        pygame.display.set_caption("Robot Server V0.1")
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)

    def _exit(self):
        self.broker.disconnect()
        pygame.quit()
        self.is_working = False

    def _clear_screen(self):
        self.sc.fill((255, 255, 255))
        pygame.display.update()

    # def _key_pressed(self, key):
    #     self._clear_screen()
    #     if key == pygame.K_UP:
    #         txt = "UP pressed"
    #     else:
    #         txt = f"{key} pressed"
    #     self._show_text(txt)
    #
    # def _key_released(self, key):
    #     self._clear_screen()
    #     if key == pygame.K_UP:
    #         txt = "UP released"
    #     else:
    #         txt = f"{key} released"
    #     self._show_text(txt)

    def _show_text(self, text, pos):
        self._clear_screen()
        text1 = self.font.render(text, True, (0, 0, 0))
        self.sc.blit(text1, pos)

        pygame.display.update()

    def _show_new_frame(self):
        pass

    def _get_actual_telemetry(self):
        packet = self.broker.get(key=Constants.REDIS_TELEMETRY_KEY)
        return self.protocol.parse_packet(packet) if packet else None

    def _fill_telemetry(self, list_of_params):
        for param in list_of_params:
            self.telemetry.__setattr__(param[0], param[1])


if __name__ == "__main__":
    server = Server()
    server.run()
