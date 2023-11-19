import subprocess
from pathlib import Path

import pygame

pygame.init()


class Display:
    def __init__(self, path: Path) -> None:
        self.PATH_ORIGIN = path

        self.max_name_per_row = 4

        self.screen = pygame.display.set_mode((1200, 600))
        # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # pygame.display.toggle_fullscreen()
        pygame.display.set_caption("explorer2")

        ICONFILE = "icon.png"
        if Path(ICONFILE).exists():
            programIcon = pygame.image.load(ICONFILE)
            pygame.display.set_icon(programIcon)

        self.WIDTH, self.HEIGHT = self.screen.get_size()
        self.BTN_WIDTH = 200
        self.BTN_HEIGHT = 50
        self.BTN_SPACE = 50

        self.COLOR_FONT = (50, 50, 50)
        self.COLOR_BACKGROUND = (255, 236, 236)
        self.COLOR_BUTTON_DIRECTORY_BACKGROUND = (205, 237, 252)
        self.COLOR_BUTTON_FILE_BACKGROUND = (255, 128, 128)

        self.FONT_BUTTON = pygame.font.SysFont("Corbel", 35)

        self.call_page(path)

    def run(self) -> None:
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.catch_event(event)
            pygame.display.flip()
        pygame.quit()

    # display page
    def call_page(self, path: Path) -> None:
        if path.suffix == ".pdf":
            self.display_file(path)
        else:
            self.display_directory(path)

    def get_pos_btn(self, nb_total: int) -> list[list[int]]:
        pos = []
        nb_list = (nb_total // self.max_name_per_row) * [self.max_name_per_row] + [
            nb_total % self.max_name_per_row
        ]
        for row in range(1 + nb_total // self.max_name_per_row):
            nb = nb_list[row]

            x = self.WIDTH // 2
            if nb % 2 == 1:
                x -= self.BTN_WIDTH // 2
            else:
                x += self.BTN_SPACE // 2

            for _ in range(nb // 2):
                x -= self.BTN_WIDTH + self.BTN_SPACE

            for _ in range(nb):
                pos.append(
                    [x, (self.HEIGHT // 4) + row * (self.BTN_HEIGHT + self.BTN_SPACE)]
                )
                x += self.BTN_WIDTH + self.BTN_SPACE
        return pos

    def display_directory(self, path):
        # background
        surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        surface.fill(self.COLOR_BACKGROUND)

        # buttons
        self.zone_button = []
        files = [file for file in path.glob("*")]
        files_pos = self.get_pos_btn(len(files))
        for i, file in enumerate(files):
            pos_button = files_pos[i] + [self.BTN_WIDTH, self.BTN_HEIGHT]
            text_button = self.FONT_BUTTON.render(file.stem, True, self.COLOR_FONT)
            textRect = text_button.get_rect()
            textRect.center = (
                pos_button[0] + self.BTN_WIDTH // 2,
                pos_button[1] + self.BTN_HEIGHT // 2,
            )
            background_color = (
                self.COLOR_BUTTON_FILE_BACKGROUND
                if file.suffix == ".pdf"
                else self.COLOR_BUTTON_DIRECTORY_BACKGROUND
            )
            pygame.draw.rect(self.screen, background_color, pos_button)
            self.screen.blit(text_button, textRect)
            self.zone_button.append((pos_button, file))

        if path != self.PATH_ORIGIN:
            text_button = self.FONT_BUTTON.render("<-", True, self.COLOR_FONT)
            pos_button = [100, 60, 150, 50]
            pygame.draw.rect(
                self.screen, self.COLOR_BUTTON_DIRECTORY_BACKGROUND, pos_button
            )
            textRect = text_button.get_rect()
            textRect.center = (
                pos_button[0] + self.BTN_WIDTH // 2,
                pos_button[1] + self.BTN_HEIGHT // 2,
            )
            self.screen.blit(text_button, textRect)
            self.zone_button.append((pos_button, path.parent))

        text_button = self.FONT_BUTTON.render(str(path), True, self.COLOR_FONT)
        self.screen.blit(text_button, [800, 60])

    def display_file(self, path):
        subprocess.Popen([path], shell=True)

    # events
    def catch_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_p:
                    self.running = False
                case _:
                    pass

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            self.catch_button(mouse)

    def catch_button(self, mouse):
        for (x1, y1, x2, y2), path in self.zone_button:
            if x1 < mouse[0] < x1 + x2 and y1 < mouse[1] < y1 + y2:
                self.call_page(path)
                break


display = Display(Path("./test/"))
display.run()
