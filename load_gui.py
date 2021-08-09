import pygame as game
from pygame.locals import *
import sys
import os
from gui import colors
from datetime import datetime

base_dir = os.path.dirname(__file__)
saves = os.path.join(base_dir, r"saves")
print('saves : ' + str(saves))

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
        self.load_dict = {}
        self.max_pages = 0
        self.cur_page = 0
        self.next_page_rect = Rect(600, 715, 180, 30)
        self.prev_page_rect = Rect(600, 740, 180, 30)
        self.back_start_page_rect = Rect(330, 740, 200, 30)

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

                status = self.check_event(event)
                if status is not None:
                    return status

            game.display.update()

    def set_game_screen(self, load_highlighted: int = -1,
                        btn_highlighted: str = '', init=False) -> None:
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

        background = game.Surface(self.surface.get_size())
        background = background.convert()
        background.fill(self.colors['dark_grey'])
        self.surface.blit(background, (0, 0))

        # draw outline
        self.render_outline(buffer, thickness, board_width, self.colors['white'])
        # write title
        self.render_load_title()
        # write back button
        self.render_button(btn_text='Back', pos=(730, 35),
                           btn_highlighted=btn_highlighted, init=init)
        # write menu choices
        self.render_load_choices(highlighted=load_highlighted, init=init)

        if self.max_pages > 0:
            if self.cur_page < self.max_pages:
                self.render_button(
                    btn_highlighted=btn_highlighted,
                    btn_text="View Next Page", pos=(600, 715)
                )
            if self.cur_page > 0:
                self.render_button(
                    btn_highlighted=btn_highlighted,
                    btn_text="View Previous Page", pos=(600, 740)
                )
                self.render_button(
                    btn_highlighted=btn_highlighted,
                    btn_text="Back to Start Page", pos=(330, 740)
                )

    def render_outline(self, buffer: int, thickness: int,
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

    def render_button(self, btn_text: str, pos: tuple,
                      btn_highlighted: str = '', init=False) -> None:
        """
        takes one parameter: highlighted (int)
        returns None

        Renders the clickable Back button

        If highlighted == 1: render back_button in highlighted_grey
        Else: render button_button in grey
        """
        back_button_rect = Rect(pos[0], pos[1], 30, 30)

        if init:
            if btn_text == 'Back':
              self.back_button_rect = back_button_rect

        font = game.font.SysFont('dubai', 20)
        button = font.render(btn_text, True, self.colors['grey'])
        button_highlighted = font.render(btn_text, True,
                                              self.colors['hl_grey'])

        if btn_highlighted == btn_text:
            self.surface.blit(button_highlighted, pos)
        else:
            self.surface.blit(button, back_button_rect)

    def render_load_title(self) -> None:
        """
        takes no parameters
        returns None

        Performs rendering for Game Title text
        """
        font = game.font.SysFont('dubai', 95)
        img = font.render('LOAD GAME', True, self.colors['off_white'])
        self.surface.blit(img, (165, 75))

    def generate_load_dict(self):
        count = 0

        for save in os.listdir(saves):
            save_date = datetime.fromtimestamp(os.path.getmtime(
                os.path.join(saves, save))
            )
            save_date = save_date.strftime("%m/%d/%Y")
            save_dict = {"name": save, "date": save_date}
            save_number = str(count)
            self.load_dict[save_number] = save_dict
            count += 1

    def handle_loads_size(self):
        no_of_loads = len(self.load_dict.keys())
        if no_of_loads > 4:
            if no_of_loads % 4 == 0:
                self.max_pages = (no_of_loads // 3) - 1
            else:
                self.max_pages = no_of_loads // 4

    def render_load_choices(self, highlighted: int = -1, init=False) -> None:
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
        self.generate_load_dict()
        self.handle_loads_size()

        # TESTING
        load_games = self.load_dict
        entries = self.load_dict.keys()

        # starting values for load game rects
        x = 50
        y = 250
        w = 700
        h = 100

        load_rect_count = 0

        # if load dict empty
        if not self.load_dict:
            load_font = game.font.SysFont('dubai', 40)
            load_rect = Rect(x, y, w, h)
            empty_text = "No Save Data"
            text = load_font.render(empty_text, True,
                                    self.colors['off_white'])
            game.draw.rect(self.surface, self.colors['white'], load_rect,
                           width=2)
            self.surface.blit(text, (x + 30, y + 20))

        # else, iterate over games in load_games (or, for testing entries) dict
        else:
            no_of_entries = len(self.load_dict.keys())
            entries_to_display = []
            if no_of_entries > 4:
                entry_no = self.cur_page * 4
                while entry_no < no_of_entries and len(entries_to_display) < 4:
                    entries_to_display.append(entry_no)
                    entry_no += 1
            else:
                for i in range(0, no_of_entries):
                    entries_to_display.append(i)

            for load_idx in entries_to_display:
                load_rect = Rect(x, y, w, h)

                # initialize self.load_game_rects list
                if init:
                    self.load_game_rects.append(load_rect)

                # establish strings for Name and Date
                name_text = 'Name: ' + self.load_dict[str(load_idx)]['name']
                date_text = 'Date Saved: ' + \
                            self.load_dict[str(load_idx)]['date']

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

    def check_event(self, event):
        if event == game.QUIT:
            game.quit()
            sys.exit()

        # If mouse motion is detected, check new position
        # If new position coincides with position of any options text,
        #   re-render text/section as 'highlighted'
        elif event.type == game.MOUSEMOTION:
            self.handle_mouse_motion_event()

        # if click, check location
        # if back button, return 'back' to render main menu
        # if a load option, for now return 'load'
        #   eventually, will return something like a load_id
        elif event.type == game.MOUSEBUTTONDOWN:
            status = self.handle_mouse_click_event()
            return status

    def handle_mouse_motion_event(self) -> None:
        load_highlighted = -1
        btn_highlighted = ''

        # get mouse pos
        mouse = game.mouse.get_pos()

        # rect count to iterate over load game rects
        rect_count = 0
        for load_rect in self.load_game_rects:
            if check_mouse_collide(mouse, load_rect):
                load_highlighted = rect_count
            rect_count += 1

        if check_mouse_collide(mouse, self.back_button_rect):
            btn_highlighted: str = 'Back'

        elif self.cur_page > 0:

            if check_mouse_collide(mouse, self.prev_page_rect):
                btn_highlighted = "View Previous Page"

            elif check_mouse_collide(mouse, self.back_start_page_rect):
                btn_highlighted = "Back to Start Page"

        elif self.max_pages > 0 and self.cur_page != self.max_pages:
            if check_mouse_collide(mouse, self.next_page_rect):
                btn_highlighted = "View Next Page"

        else:
            if btn_highlighted != '':
                btn_highlighted: str = ''

        self.set_game_screen(load_highlighted=load_highlighted,
                             btn_highlighted=btn_highlighted)

    def handle_mouse_click_event(self) -> str:
        mouse = game.mouse.get_pos()
        click = game.mouse.get_pressed(3)
        if click[0] == 1:
            for load_rect in self.load_game_rects:
                if check_mouse_collide(mouse, load_rect):
                    load_idx = str(
                        self.load_game_rects.index(load_rect) +
                        (self.cur_page * 4))
                    load_name = self.load_dict[load_idx]["name"]
                    return load_name

            if check_mouse_collide(mouse, self.back_button_rect):
                return 'back'

            if self.cur_page > 0:
                if check_mouse_collide(mouse, self.prev_page_rect):
                    self.cur_page -= 1
                    self.set_game_screen()

                if check_mouse_collide(mouse, self.back_start_page_rect):
                    self.cur_page = 0
                    self.set_game_screen()

            if self.max_pages > 0 and self.cur_page != self.max_pages:
                if check_mouse_collide(mouse, self.next_page_rect):
                    self.cur_page += 1
                    self.set_game_screen()
