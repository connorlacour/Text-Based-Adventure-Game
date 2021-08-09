import pygame as game
from pygame.locals import *
import sys
from gui import colors
import os
from datetime import datetime

base_dir = os.path.dirname(__file__)
saves = os.path.join(base_dir, r"saves")


# STATIC FUNCTIONS
def validate_user_entry(user_entry: str):
    valid_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                   'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                   'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
                   'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                   'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3',
                   '4', '5', '6', '7', '8', '9', '0', '-', '_']
    if user_entry == 'back':
        return False

    for char in user_entry:
        if char not in valid_chars:
            print(char, ' is an invalid character!')
            return False

    return True


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


def generate_save_games_test_data():
    # I don't know how the Object will be structured, this is
    #   just to populate sample data just as "proof of concept"
    test_data = {}
    save_1 = {'name': 'Connor', 'date': '07/04/21'}
    save_2 = {'name': 'Caroline', 'date': '07/01/21'}

    test_data['Save 1'] = save_1
    test_data['Save 2'] = save_2

    return test_data


class SaveGUI:
    def __init__(self):
        self.window_height = 800
        self.surface = game.display.set_mode((800, 800))
        self.colors = colors.Colors().get_colors()
        self.save_game_rects = []
        self.back_button_rect = None
        self.next_page_rect = Rect(600, 715, 180, 30)
        self.prev_page_rect = Rect(600, 740, 180, 30)
        self.back_start_page_rect = Rect(330, 740, 200, 30)
        self.save_dict = {}
        self.cur_page = 0
        self.max_pages = 0
        self.user_entry = ''
        self.cancel_highlighted = ''

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

        # fill background with black
        background = game.Surface(self.surface.get_size())
        background = background.convert()
        background.fill(self.colors['dark_grey'])

        # Blit background to the screen
        self.surface.blit(background, (0, 0))
        game.display.flip()
        self.set_game_screen(init=True)
        game.display.update()

        # while 1 loop maintains display updates and should only terminate
        #   upon game ending
        while 1:
            # Constant check for game.QUIT
            for event in game.event.get():

                status = self.check_event(event)
                if status is not None:
                    return status

            game.display.update()

    def set_game_screen(self, save_highlighted: int = -1,
                        btn_highlighted: str = '', init=False) -> None:
        """
        takes 3 optional parameters:
            save_highlighted with a default state of -1
            btn_highlighted with a default state of ''
            init with a default state of False
        Returns None

        Renders game screen and calls all component rendering functions
            including: draw_outline(), write_save_title(),
            write_back_button(), & display_menu_choices()

        If init=True, save_game_rects and back_button_rect are generated
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
        self.render_save_title()
        # write back button
        self.render_button(btn_text='Back', pos=(730, 35),
                           btn_highlighted=btn_highlighted, init=init)

        # write menu choices
        self.render_save_choices(highlighted=save_highlighted, init=init)

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

    def generate_save_dict(self):
        count = 0

        if "saves" not in os.listdir(base_dir):
            os.mkdir(os.path.join(base_dir, "saves"))

        for save in os.listdir(saves):
            save_date = datetime.fromtimestamp(os.path.getmtime(
                os.path.join(saves, save))
            )
            save_date = save_date.strftime("%m/%d/%Y")
            save_dict = {"name": save, "date": save_date}
            save_number = str(count)
            self.save_dict[save_number] = save_dict
            count += 1

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
        button_rect = Rect(pos[0], pos[1], 30, 30)

        if init:
            if btn_text == 'Back':
                self.back_button_rect = button_rect

        font = game.font.SysFont('dubai', 20)
        if btn_text == 'Cancel':
            button = font.render(btn_text, True, self.colors['darker_grey'])
            button_highlighted = font.render(btn_text,
                                             True, self.colors['hl_dark_grey'])
        else:
            button = font.render(btn_text, True, self.colors['grey'])
            button_highlighted = font.render(btn_text,
                                             True, self.colors['hl_grey'])

        if btn_highlighted == btn_text:
            self.surface.blit(button_highlighted, button_rect)
        else:
            self.surface.blit(button, button_rect)

    def render_save_title(self) -> None:
        """
        takes no parameters
        returns None

        Performs rendering for Game Title text
        """
        font = game.font.SysFont('dubai', 95)
        img = font.render('SAVE GAME', True, self.colors['off_white'])
        self.surface.blit(img, (165, 75))

    def new_save_entry(self) -> str:
        self.render_new_save_box()

        # enter while loop for new save text entry
        while 1:
            for event in game.event.get():
                entry_status = self.check_event_in_save_entry(event)
                if entry_status is not None:
                    return entry_status
                game.display.update()

    def render_text_entry(self, user_text: str):
        font = game.font.SysFont('dubai', 26)
        user_entry = font.render(user_text, True, self.colors['off_white'])
        text_entry_rect = Rect(60, 430, 680, 40)
        game.draw.rect(self.surface, color=self.colors['dark_grey'],
                       rect=text_entry_rect)
        self.surface.blit(user_entry, (65, 435))

    def render_new_save_box(self):
        # init and render entry box & outline
        new_save_rect = Rect(40, 360, 720, 390)
        new_save_rect_outline = Rect(44, 364, 712, 382)
        text_entry_rect = Rect(60, 430, 680, 40)

        game.draw.rect(self.surface, color=self.colors['grey'],
                       rect=new_save_rect)
        game.draw.rect(self.surface, color=self.colors['dark_grey'],
                       rect=new_save_rect_outline, width=4)
        game.draw.rect(self.surface, color=self.colors['dark_grey'],
                       rect=text_entry_rect)

        # render prompt
        save_prompt_text = 'Enter save file name: '
        font = game.font.SysFont('dubai', 26)
        save_prompt = font.render(save_prompt_text, True,
                                  self.colors['darker_grey'])
        self.surface.blit(save_prompt, (60, 380))

        # render cancel btn
        self.render_button('Cancel', pos=(670, 700))

    def handle_saves_size(self):
        no_of_saves = len(self.save_dict.keys())
        if no_of_saves > 3:
            if no_of_saves % 3 == 0:
                self.max_pages = (no_of_saves // 3) - 1
            else:
                self.max_pages = no_of_saves // 3

    def render_save_choices(self, highlighted: int = -1, init=False) -> None:
        """
        takes 3 optional parameters:
            highlighted with default state of -1
            init with default state of False
        Returns None

        Performs rendering for save choice text
        Renders based on mouse_pos() as determined by and called in main()
        """
        save_font = game.font.SysFont('dubai', 26)
        new_save_font = game.font.SysFont('dubai', 50)

        self.generate_save_dict()
        self.handle_saves_size()

        # starting values for save game rects
        x = 50
        y = 250
        w = 700
        h = 100

        save_rect_count = 0
        save_rect = Rect(x, y, w, h)

        if init:
            self.save_game_rects.append(save_rect)

        save_text = 'New Save'
        game.draw.rect(self.surface, self.colors['white'], save_rect,
                       width=2)
        save_rect = Rect(x + 2, y + 2, w - 4, h - 4)

        if highlighted == save_rect_count:
            game.draw.rect(self.surface, self.colors['hl_dark_grey'],
                           save_rect)
        else:
            game.draw.rect(self.surface, self.colors['grey'],
                           save_rect)
        name = new_save_font.render(save_text, True,
                                    self.colors['off_white'])
        self.surface.blit(name, (300, y + 10))

        # increment positional arguments (y) and count
        y += (h + 20)
        save_rect_count += 1

        # determine how many entries to display and their respective indices
        no_of_entries = len(self.save_dict.keys())
        entries_to_display = []
        if no_of_entries > 3:
            entry_no = self.cur_page * 3
            while entry_no < no_of_entries and len(entries_to_display) < 3:
                entries_to_display.append(entry_no)
                entry_no += 1
        else:
            for i in range(0, no_of_entries):
                entries_to_display.append(i)

        # iterate over games in save_games
        for save_idx in entries_to_display:
            save_rect = Rect(x, y, w, h)

            # initialize self.save_game_rects list
            if init:
                self.save_game_rects.append(save_rect)

            # establish strings for Name and Date
            name_text = 'Name: ' + self.save_dict[str(save_idx)]['name']
            date_text = 'Date Saved: ' + self.save_dict[str(save_idx)]['date']

            # if highlighted, render rects and text with highlight colors
            if highlighted == save_rect_count:
                # outline of rect
                game.draw.rect(self.surface, self.colors['white'],
                               save_rect, width=2)

                # interior fill of rect
                save_rect = Rect(x + 2, y + 2, w - 4, h - 4)
                game.draw.rect(self.surface, self.colors['hl_dark_grey'],
                               save_rect)
                name = save_font.render(name_text, True,
                                        self.colors['off_white'])
                date_saved = save_font.render(date_text, True,
                                              self.colors['off_white'])
                self.surface.blit(name, (x + 10, y + 10))
                self.surface.blit(date_saved, (x + 10, y + 50))

            # Else, render rects and text with standard colors
            else:
                # outline of rect
                game.draw.rect(self.surface, self.colors['off_white'],
                               save_rect, width=2)

                # interior of rect
                save_rect = Rect(x + 2, y + 2, w - 4, h - 4)
                game.draw.rect(self.surface, self.colors['grey'],
                               save_rect)

                name = save_font.render(name_text, True,
                                        self.colors['off_white'])
                date_saved = save_font.render(date_text, True,
                                              self.colors['off_white'])
                self.surface.blit(name, (x + 10, y + 10))
                self.surface.blit(date_saved, (x + 10, y + 50))

            # increment positional arguments (y) and count
            y += (h + 20)
            save_rect_count += 1

    def check_event_in_save_entry(self, event):
        cancel_btn_rect = Rect(670, 700, 50, 30)

        if event == game.QUIT:
            game.quit()
            sys.exit()

        elif event.type == game.MOUSEMOTION:
            mouse = game.mouse.get_pos()
            if check_mouse_collide(mouse, cancel_btn_rect):
                self.cancel_highlighted = 'Cancel'
                self.render_button('Cancel', pos=(670, 700),
                                   btn_highlighted=self.cancel_highlighted)
            else:
                if self.cancel_highlighted != '':
                    self.cancel_highlighted = ''
                    self.render_button('Cancel', pos=(670, 700),
                                       btn_highlighted=self.cancel_highlighted)
                    self.render_new_save_box()

        elif event.type == game.MOUSEBUTTONDOWN:
            mouse = game.mouse.get_pos()
            click = game.mouse.get_pressed(3)
            if check_mouse_collide(mouse, cancel_btn_rect):
                if click[0] == 1:
                    return 'cancelled'

        elif event.type == game.KEYDOWN:
            if self.user_entry != '':
                if event.key == game.K_BACKSPACE:
                    self.user_entry = self.user_entry[:-1]
                elif event.key == game.K_RETURN:
                    if validate_user_entry(self.user_entry):
                        return self.user_entry
                    else:
                        print('invalid save name!')
                        self.user_entry = ''
                else:
                    self.user_entry += event.unicode
            elif event.key != game.K_BACKSPACE and \
                    event.key != game.K_RETURN:
                self.user_entry += event.unicode

            self.render_text_entry(user_text=self.user_entry)

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
        # if a save option, for now return 'save'
        #   eventually, will return something like a save_id
        elif event.type == game.MOUSEBUTTONDOWN:
            status = self.handle_mouse_click_event()
            return status

    def handle_mouse_motion_event(self):
        save_highlighted = -1
        btn_highlighted = ''

        # get mouse pos
        mouse = game.mouse.get_pos()

        # rect count to iterate over save game rects
        rect_count = 0
        for save_rect in self.save_game_rects:
            if check_mouse_collide(mouse, save_rect):
                save_highlighted = rect_count
            rect_count += 1

        # Check for highlight over Back Button
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

        self.set_game_screen(save_highlighted=save_highlighted,
                             btn_highlighted=btn_highlighted)

    def handle_mouse_click_event(self):
        mouse = game.mouse.get_pos()
        click = game.mouse.get_pressed(3)
        if click[0] == 1:
            for save_rect in self.save_game_rects:
                if save_rect == self.save_game_rects[0]:
                    if check_mouse_collide(mouse, save_rect):
                        save_status: str = self.new_save_entry()
                        if save_status == 'cancelled':
                            return 'refresh'
                        else:
                            return save_status
                elif check_mouse_collide(mouse, save_rect):
                    idx = str(self.save_game_rects.index(
                        save_rect) + (self.cur_page * 3) - 1
                              )
                    save_name = self.save_dict[idx]["name"]
                    return save_name

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

