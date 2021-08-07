import pygame as game
from pygame.locals import *
import sys
import colors


# STATIC FUNCTIONS

def check_mouse_collide(mouse: tuple, rect: Rect) -> bool:
    """
    Takes 2 arguments:
        mouse of type tuple which represents the current position of mouse
        rect of type Rect

    If mouse is colliding with rect: return True
    Else: return False
    """
    if rect.collidepoint(mouse):
        return True
    return False


def load_games_test_data():
    # I don't know how the Object will be structured, this is
    #   just to populate sample data just as "proof of concept"
    test_data = {}
    load_1 = {'name': 'Connor', 'date': '07/04/21'}
    load_2 = {'name': 'Caroline', 'date': '07/01/21'}
    load_3 = {'name': 'Emily', 'date': '07/10/21'}

    test_data['Load 1'] = load_1
    test_data['Load 2'] = load_2
    test_data['Load 3'] = load_3

    return test_data


class LoadGameGUI:
    def __init__(self):
        self.window_height = 800
        self.surface = game.display.set_mode((800, 800))
        self.colors = colors.Colors().get_colors()
        self.load_game_rects = []
        self.back_button_rect = None

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
        self.set_game_screen(init=True)

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
                #   re-render text/section as 'highlighted'
                elif event.type == game.MOUSEMOTION:
                    load_highlighted = -1
                    back_highlighted = -1

                    # get mouse pos
                    mouse = game.mouse.get_pos()

                    # rect count to iterate over load game rects
                    rect_count = 0
                    for load_rect in self.load_game_rects:
                        if check_mouse_collide(mouse, load_rect):
                            load_highlighted = rect_count
                        rect_count += 1

                    # Check for highlight over Back Button
                    if check_mouse_collide(mouse, self.back_button_rect):
                        # highlighted = 1 will render the back_button as
                        #   'highlighted_grey'
                        back_highlighted: int = 1

                        # entire game_screen must be re-rendered, so we must
                        #   ensure that all components are appropriately
                        #   maintained
                        self.set_game_screen(back_highlighted=back_highlighted)
                    else:
                        # only perform re-render if back_button was previously
                        #   highlighted
                        if back_highlighted == 1:
                            back_highlighted: int = -1

                            # entire game_screen must be re-rendered, so we
                            #   must ensure that the scroll text and all other
                            #   components are appropriately maintained
                            self.set_game_screen(
                                back_highlighted=back_highlighted)
                    self.set_game_screen(load_highlighted=load_highlighted,
                                         back_highlighted=back_highlighted)

                # if click, check location
                # if back button, return 'back' to render main menu
                # if a load option, for now return 'load'
                #   eventually, will return something like a load_id
                elif event.type == game.MOUSEBUTTONDOWN:
                    mouse = game.mouse.get_pos()
                    click = game.mouse.get_pressed(3)
                    if click[0] == 1:
                        for load_rect in self.load_game_rects:
                            if check_mouse_collide(mouse, load_rect):
                                return 'load'

                        if check_mouse_collide(mouse, self.back_button_rect):
                            return 'back'
            game.display.update()

    def set_game_screen(self, load_highlighted: int = -1,
                        back_highlighted: int = -1, init=False) -> None:
        """
        takes 3 optional parameters:
            load_highlighted with a default state of -1
            back_highlighted with a default state of -1
            init with a default state of False
        Returns None

        Renders game screen and calls all component rendering functions
            including: draw_outline(), write_load_title(),
            write_back_button(), & display_menu_choices()

        If init=True, load_game_rects and back_button_rect are generated
        If init=False, rects are expected to already exist
        """

        # local vars for draw_outline
        buffer: int = 25
        screen_width: int = self.window_height
        board_width: int = screen_width - (2 * buffer)
        thickness: int = 3

        # draw outline
        self.draw_outline(buffer, thickness, board_width, self.colors['white'])
        # write title
        self.write_load_title()
        # write back button
        self.write_back_button(highlighted=back_highlighted, init=init)
        # write menu choices
        self.display_load_choices(highlighted=load_highlighted, init=init)

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

    def write_back_button(self, highlighted: int = -1, init=False) -> None:
        """
        takes one parameter: highlighted (int)
        returns None

        Renders the clickable Back button

        If highlighted == 1: render back_button in highlighted_grey
        Else: render button_button in grey
        """
        back_button_rect = Rect(730, 35, 30, 30)

        if init:
            self.back_button_rect = back_button_rect

        font = game.font.SysFont('dubai', 20)
        back_button = font.render('Back', True, self.colors['grey'])
        back_button_highlighted = font.render('Back', True,
                                              self.colors['hl_grey'])
        self.surface.blit(back_button, (730, 35))

        if highlighted == 1:
            self.surface.blit(back_button_highlighted, (730, 35))
        else:
            self.surface.blit(back_button, back_button_rect)

    def write_load_title(self) -> None:
        """
        takes no parameters
        returns None

        Performs rendering for Game Title text
        """
        font = game.font.SysFont('dubai', 95)
        img = font.render('LOAD GAME', True, self.colors['off_white'])
        self.surface.blit(img, (165, 75))

    def display_load_choices(self, highlighted: int = -1,
                             load_games: dict = None, init=False) -> None:
        """
        takes 3 optional parameters:
            highlighted with default state of -1
            load_games of type dict with default state of None
                load_games will eventually be populated by BE
            init with default state of False
        Returns None

        Performs rendering for load choice text
        Renders based on mouse_pos() as determined by and called in main()
        """
        load_font = game.font.SysFont('dubai', 26)

        # TESTING
        load_games = load_games_test_data()
        entries = load_games.keys()

        # starting values for load game rects
        x = 50
        y = 250
        w = 700
        h = 100

        # cou
        load_rect_count = 0

        # iterate over games in load_games (or, for testing entries) dict
        for games in entries:
            load_rect = Rect(x, y, w, h)

            # initialize self.load_game_rects list
            if init:
                self.load_game_rects.append(load_rect)

            # establish strings for Name and Date
            name_text = 'Name: ' + load_games[games]['name']
            date_text = 'Date Saved: ' + load_games[games]['date']

            # if highlighted, render rects and text with highlight colors
            if highlighted == load_rect_count:
                # outline of rect
                game.draw.rect(self.surface, self.colors['white'], load_rect,
                               width=2)

                # interior fill of rect
                load_rect = Rect(x + 2, y + 2, w - 4, h - 4)
                game.draw.rect(self.surface, self.colors['dark_grey'],
                               load_rect)
                name = load_font.render(name_text, True,
                                        self.colors['off_white'])
                date = load_font.render(date_text, True,
                                        self.colors['off_white'])
                self.surface.blit(name, (x + 10, y + 10))
                self.surface.blit(date, (x + 10, y + 50))

            # Else, render rects and text with standard colors
            else:
                # outline of rect
                game.draw.rect(self.surface, self.colors['off_white'],
                               load_rect, width=2)

                # interior of rect
                load_rect = Rect(x + 2, y + 2, w - 4, h - 4)
                game.draw.rect(self.surface, self.colors['black'],
                               load_rect)

                name = load_font.render(name_text, True,
                                        self.colors['off_white'])
                date = load_font.render(date_text, True,
                                        self.colors['off_white'])
                self.surface.blit(name, (x + 10, y + 10))
                self.surface.blit(date, (x + 10, y + 50))

            # increment positional arguments (y) and count
            y += (h + 20)
            load_rect_count += 1
