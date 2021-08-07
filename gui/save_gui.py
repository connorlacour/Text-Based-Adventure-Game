import pygame as game
from pygame.locals import *
import sys
import colors
#  from datetime import date


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
        self.save_game_data = generate_save_games_test_data()

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
        background.fill(self.colors['dark_grey'])

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
                    save_highlighted = -1
                    back_highlighted = -1

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
                    self.set_game_screen(save_highlighted=save_highlighted,
                                         back_highlighted=back_highlighted)

                # if click, check location
                # if back button, return 'back' to render main menu
                # if a save option, for now return 'save'
                #   eventually, will return something like a save_id
                elif event.type == game.MOUSEBUTTONDOWN:
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
                                return 'save'

                        if check_mouse_collide(mouse, self.back_button_rect):
                            return 'back'
            game.display.update()

    def set_game_screen(self, save_highlighted: int = -1,
                        back_highlighted: int = -1, init=False) -> None:
        """
        takes 3 optional parameters:
            save_highlighted with a default state of -1
            back_highlighted with a default state of -1
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

        # draw outline
        self.draw_outline(buffer, thickness, board_width, self.colors['white'])
        # write title
        self.write_save_title()
        # write back button
        self.write_button(btn_text='Back', pos=(730, 35),
                          highlighted=back_highlighted, init=init)
        # write menu choices
        self.display_save_choices(highlighted=save_highlighted, init=init)

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

    def write_button(self, btn_text: str, pos: tuple, highlighted: int = -1,
                     init=False) -> None:
        """
        takes one parameter: highlighted (int)
        returns None

        Renders the clickable Back button

        If highlighted == 1: render back_button in highlighted_grey
        Else: render button_button in grey
        """
        button_rect = Rect(pos[0], pos[1], 30, 30)

        if init:
            self.back_button_rect = button_rect

        font = game.font.SysFont('dubai', 20)
        back_button = font.render(btn_text, True, self.colors['grey'])
        back_button_highlighted = font.render(btn_text, True,
                                              self.colors['hl_grey'])
        self.surface.blit(back_button, pos)

        if highlighted == 1:
            self.surface.blit(back_button_highlighted, pos)
        else:
            self.surface.blit(back_button, button_rect)

    def write_save_title(self) -> None:
        """
        takes no parameters
        returns None

        Performs rendering for Game Title text
        """
        font = game.font.SysFont('dubai', 95)
        img = font.render('SAVE GAME', True, self.colors['off_white'])
        self.surface.blit(img, (165, 75))

    def new_save_entry(self) -> str:
        cancel_btn_rect = Rect(670, 700, 50, 30)
        self.render_new_save_box()

        # loop vars
        user_text: str = ''
        cancel_highlighted: int = 0

        # enter while loop for new save text entry
        while 1:
            for event in game.event.get():
                if event == game.QUIT:
                    game.quit()
                    sys.exit()

                elif event.type == game.MOUSEMOTION:
                    mouse = game.mouse.get_pos()
                    if check_mouse_collide(mouse, cancel_btn_rect):
                        cancel_highlighted = 1
                        self.write_button('Cancel', pos=(670, 700),
                                          highlighted=cancel_highlighted)
                    else:
                        if cancel_highlighted == 1:
                            cancel_highlighted = 0
                            self.write_button('Cancel', pos=(670, 700),
                                              highlighted=cancel_highlighted)

                elif event.type == game.MOUSEBUTTONDOWN:
                    mouse = game.mouse.get_pos()
                    click = game.mouse.get_pressed(3)
                    if check_mouse_collide(mouse, cancel_btn_rect):
                        if click[0] == 1:
                            return 'cancelled'

                elif event.type == game.KEYDOWN:
                    if user_text != '':
                        if event.key == game.K_BACKSPACE:
                            user_text = user_text[:-1]
                        elif event.key == game.K_RETURN:
                            return user_text
                        else:
                            user_text += event.unicode
                    elif event.key != game.K_BACKSPACE and \
                            event.key != game.K_RETURN:
                        user_text += event.unicode

                    self.render_text_entry(user_text=user_text)

                game.display.update()

    def render_text_entry(self, user_text: str):
        font = game.font.SysFont('dubai', 26)
        user_entry = font.render(user_text, True, self.colors['off_white'])
        text_entry_rect = Rect(60, 430, 680, 40)
        game.draw.rect(self.surface, color=self.colors['darker_grey'],
                       rect=text_entry_rect)
        self.surface.blit(user_entry, (65, 435))

    def render_new_save_box(self):
        # init and render entry box & outline
        new_save_rect = Rect(40, 360, 720, 390)
        new_save_rect_outline = Rect(44, 364, 712, 382)
        text_entry_rect = Rect(60, 430, 680, 40)

        game.draw.rect(self.surface, color=self.colors['hl_dark_grey'],
                       rect=new_save_rect)
        game.draw.rect(self.surface, color=self.colors['dark_grey'],
                       rect=new_save_rect_outline, width=4)
        game.draw.rect(self.surface, color=self.colors['darker_grey'],
                       rect=text_entry_rect)

        # render prompt
        save_prompt_text = 'Enter save file name: '
        font = game.font.SysFont('dubai', 26)
        save_prompt = font.render(save_prompt_text, True,
                                  self.colors['off_white'])
        self.surface.blit(save_prompt, (60, 380))

        # render cancel btn
        self.write_button('Cancel', pos=(670, 700))

    def display_save_choices(self, highlighted: int = -1, init=False) -> None:
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

        # TESTING
        entries = self.save_game_data.keys()

        # starting values for save game rects
        x = 50
        y = 250
        w = 700
        h = 100

        # count
        save_rect_count = 0

        # New save
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

        # iterate over games in save_games (or, for testing entries) dict
        for games in entries:
            save_rect = Rect(x, y, w, h)

            # initialize self.save_game_rects list
            if init:
                self.save_game_rects.append(save_rect)

            # establish strings for Name and Date
            name_text = 'Name: ' + self.save_game_data[games]['name']
            date_text = 'Date Saved: ' + self.save_game_data[games]['date']

            # if highlighted, render rects and text with highlight colors
            if highlighted == save_rect_count:
                # outline of rect
                game.draw.rect(self.surface, self.colors['white'], save_rect,
                               width=2)

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
