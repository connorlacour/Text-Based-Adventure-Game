import pygame as game
from pygame.locals import *
import sys
import colors


class MainMenuGUI:
    def __init__(self):
        self.window_height = 800
        self.surface = game.display.set_mode((800, 800))
        self.colors = colors.Colors().get_colors()

    def main(self) -> str:
        """
        Takes no parameters
        Returns str based on game.MOUSEBUTTONDOWN event

        Initializes game screen & maintains main while loop that listens for
            events from game.event.get()
        """

        # initialize basic screen components
        game.init()
        game.display.set_caption('GAME TITLE')

        # fill background with brown
        background = game.Surface(self.surface.get_size())
        background = background.convert()
        background.fill(self.colors['black'])

        # Blit background to the screen
        self.surface.blit(background, (0, 0))
        game.display.flip()
        self.set_game_screen()

        # while 1 loop maintains display updates and should only terminate
        #   upon game ending
        while 1:
            # Constant check for game.QUIT
            for event in game.event.get():
                if event == game.QUIT:
                    game.quit()
                    sys.exit()

                # If mouse motion is detected, check new position
                # If new position coincides with position of any options text,
                #   re-render text as 'highlighted'
                elif event.type == game.MOUSEMOTION:
                    mouse = game.mouse.get_pos()
                    if 520 > mouse[0] > 280 and 470 > mouse[1] > 420:
                        highlighted = 1
                    elif 520 > mouse[0] > 270 and 570 > mouse[1] > 520:
                        highlighted = 2
                    elif 440 > mouse[0] > 350 and 670 > mouse[1] > 620:
                        highlighted = 3
                    else:
                        highlighted = 0
                    self.set_game_screen(highlighted)

                elif event.type == game.MOUSEBUTTONDOWN:
                    mouse = game.mouse.get_pos()
                    click = game.mouse.get_pressed()
                    if 520 > mouse[0] > 280 and 470 > mouse[1] > 420:
                        if click[0] == 1:
                            print('clicked new game')
                            return 'new game'
                    elif 520 > mouse[0] > 270 and 570 > mouse[1] > 520:
                        if click[0] == 1:
                            return 'load game'
                    elif 440 > mouse[0] > 350 and 670 > mouse[1] > 620:
                        print('clicked exit')
                        return 'exit'

            game.display.update()

    def set_game_screen(self, highlighted: int = 0) -> None:
        """
        takes 1 optional parameter: highlighted with a default state of 0
        Returns None

        Renders game screen and calls all component rendering functions
            including: draw_outline(), write_game_title(),
            & write_menu_choices()
        """

        # local vars for draw_outline
        buffer: int = 25
        screen_width: int = self.window_height
        board_width: int = screen_width - (2 * buffer)
        thickness: int = 3

        # draw outline
        self.draw_outline(buffer, thickness, board_width, self.colors['white'])

        # write title
        self.write_game_title()

        # write menu choices
        self.write_menu_choices(highlighted=highlighted)

    def draw_outline(self, buffer: int, thickness: int,
                     board_width: int, color: tuple) -> None:
        """
        Takes 4 parameters: buffer, thickness, board_width, color
        Returns None

        Renders game screen outline based on parameters provided by
            set_game_screen()
        """

        outline = Rect(buffer - thickness, buffer - thickness,
                       (board_width + (2 * thickness)),
                       board_width + (2 * thickness))

        game.draw.rect(surface=self.surface, color=color,
                       rect=outline, width=thickness)

    def write_game_title(self) -> None:
        """
        takes no parameters
        returns None

        Performs rendering for Game Title text
        """
        font = game.font.SysFont('dubai', 95)
        img = font.render('G A M E T I T L E', True, self.colors['off_white'])
        self.surface.blit(img, (60, 75))

        # To get available fonts..
        #
        # fonts = game.font.get_fonts()
        # print(fonts)
        #

    def write_menu_choices(self, highlighted: int = 0) -> None:
        """
        takes one optional parameter: highlighted
            highlighted = 0 -> Default/Nothing highlighted
            highlighted = 1 -> New Game
            highlighted = 2 -> Load Game
            highlighted = 3 -> Exit
        Returns None

        Performs rendering for menu choice text
        Renders based on mouse_pos() as determined by and called in main()
        """
        font = game.font.SysFont('dubai', 55)

        new_game = font.render('New Game', True, self.colors['off_white'])
        new_game_highlight = font.render('New Game', True,
                                         self.colors['hl_dark_grey'])
        load_game = font.render('Load Game', True, self.colors['off_white'])
        load_game_highlighted = font.render('Load Game', True,
                                            self.colors['hl_dark_grey'])
        exit_game = font.render('Exit', True, self.colors['off_white'])
        exit_game_highlight = font.render('Exit', True,
                                          self.colors['hl_dark_grey'])

        if highlighted == 1:
            self.surface.blit(new_game_highlight, (280, 400))
        else:
            self.surface.blit(new_game, (280, 400))

        if highlighted == 2:
            self.surface.blit(load_game_highlighted, (270, 500))
        else:
            self.surface.blit(load_game, (270, 500))

        if highlighted == 3:
            self.surface.blit(exit_game_highlight, (350, 600))
        else:
            self.surface.blit(exit_game, (350, 600))
