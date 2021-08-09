import pygame as game
from pygame.locals import *
import sys
from gui import colors
import gui.text_scroll as scroll


class GameEnd:
    def __init__(self, status):
        self.status = status
        self.window_height = 800
        self.surface = game.display.set_mode((800, 800))
        self.scroll = scroll.Scroll(0)
        self.colors: dict = colors.Colors().get_colors()
        self.highlighted = ''

    def main(self):
        # initialize basic screen components
        game.init()
        game.display.set_caption('GAME TITLE')

        # fill background with black
        background = game.Surface(self.surface.get_size())
        background = background.convert()
        background.fill(self.colors['dark_grey'])

        # Blit background to the screen
        self.surface.blit(background, (0, 0))
        game.display.flip()

        self.set_game_screen()

        while 1:
            for event in game.event.get():
                status = self.check_event(event=event)
                if status is not None:
                    return status

                self.set_game_screen()
                game.display.update()

    def set_game_screen(self):
        rect = Rect(120, 120, 560, 560)
        outline = Rect(124, 124, 552, 552)

        game.draw.rect(self.surface, self.colors['grey'], rect)
        game.draw.rect(self.surface, self.colors['dark_grey'], outline,
                       width=3)

        if self.status == '_game_over_':
            self.title("Try Again", (250, 240))
            self.render_button("Main Menu", (180, 490))
            self.render_button("Load Game", (420, 490))
        elif self.status == '_game_win_':
            self.title("You Won!", (245, 160))
            self.render_button("Main Menu", (310, 600))
            self.render_credits()

    def title(self, title_text: str, pos: tuple):
        font = game.font.SysFont('dubai', 80)
        font2 = game.font.SysFont('dubai', 80)

        title_render = font2.render(title_text, True, self.colors['med_grey'])
        self.surface.blit(title_render, ((pos[0] - 2), (pos[1] + 3)))

        title_render = font.render(title_text, True, self.colors['off_white'])
        self.surface.blit(title_render, pos)

    def render_credits(self):
        font = game.font.SysFont('dubai', 30)
        game_credits = [
            'Thanks for playing :)',
            '',
            'Capstone Project // OSU 2021',
            '',
            'Caroline Borden',
            'Connor LaCour',
            'Emily Sorg'
        ]

        y = 320

        for line in game_credits:
            x = 370
            length = len(line)
            if length > 0:
                x = x - (length * 5)
            pos = (x, y)
            render = font.render(line, True, self.colors["offer_white"])
            self.surface.blit(render, pos)
            y = y + 30

        please = "please hire us"
        font2 = game.font.SysFont('dubai', 15)
        render2 = font2.render(please, True, (175, 175, 175))
        self.surface.blit(render2, (550, 640))

    def render_button(self, btn_text: str, pos: tuple) -> None:
        """
        takes one parameter: highlighted (int)
        returns None

        Renders the clickable Exit button

        If highlighted == 1: render exit_button in highlighted_grey
        Else: render exit_button in grey
        """
        font = game.font.SysFont('dubai', 40)
        button = font.render(btn_text, True, self.colors['offer_white'])
        button_highlighted = font.render(btn_text, True,
                                         self.colors['dark_grey'])
        self.surface.blit(button, pos)

        if self.highlighted == btn_text:
            self.surface.blit(button_highlighted, pos)
        else:
            self.surface.blit(button, pos)

    def check_event(self, event):
        """
        abstraction of GUI while game loop
        calls one of the following based on game events:
            self.handle_mouse_motion_event()
            self.handle_mouse_click_event()
            self.handle_keydown_event()
        returns None
        """
        if event.type == game.QUIT:
            game.quit()
            sys.exit()

        elif event.type == game.MOUSEMOTION:
            self.handle_mouse_motion_event()

        elif event.type == game.MOUSEBUTTONDOWN:
            status = self.handle_mouse_click_event()
            if status is not None:
                return status

    def handle_mouse_motion_event(self):
        mouse = game.mouse.get_pos()

        if self.status == '_game_over_':
            if 360 > mouse[0] > 180 and 540 > mouse[1] > 505:
                self.highlighted: str = 'Main Menu'
            elif 600 > mouse[0] > 420 and 540 > mouse[1] > 505:
                self.highlighted: str = 'Load Game'
            else:
                if self.highlighted != '':
                    self.highlighted: str = ''

        elif self.status == '_game_win_':
            if 490 > mouse[0] > 310 and 640 > mouse[1] > 605:
                self.highlighted = 'Main Menu'
            else:
                if self.highlighted != '':
                    self.highlighted: str = ''

        self.set_game_screen()

    def handle_mouse_click_event(self):
        click = game.mouse.get_pressed(3)
        mouse = game.mouse.get_pos()

        if click[0] == 1:
            if self.status == '_game_over_':
                if 360 > mouse[0] > 180 and 540 > mouse[1] > 505:
                    return 'main menu'
                elif 600 > mouse[0] > 420 and 540 > mouse[1] > 505:
                    return 'load'
            elif self.status == '_game_win_':
                if 490 > mouse[0] > 310 and 640 > mouse[1] > 605:
                    return 'main menu'


# test = GameEnd('_game_win_').main()
