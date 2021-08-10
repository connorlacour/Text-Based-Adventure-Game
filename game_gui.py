import pygame as game
from pygame.locals import *
import sys
import save_gui
from gui import colors
import gui.text_scroll as scroll
from game_objects.game_loop import *
import save_load
from math import ceil

base_dir = os.path.dirname(__file__)
saves = os.path.join(base_dir, r"saves")


class GameGUI:
    def __init__(self, is_load: bool, load_name: str=''):
        self.window_height = 800
        self.surface = game.display.set_mode((800, 800))
        self.scroll = scroll.Scroll(0)
        self.colors: dict = colors.Colors().get_colors()
        self.game_typing: bool = False
        self.scroll_page: int = 0
        self.user_entry: str = ''
        self.highlighted: str = ''
        self.game_start = True
        self.is_load = is_load
        self.load_name = load_name
        self.game_over = False
        self.game_win = False

    def main(self) -> str:
        """
        Takes no parameters
        Returns str based on game.MOUSEBUTTONDOWN event

        Initializes game screen & maintains main while loop that listens for
            events from game.event.get()

        events accounted for include:
            game.QUIT
            game.MOUSEMOTION
            game.MOUSEBUTTONDOWN
            game.KEYDOWN
        """

        # initialize basic screen components
        game.init()
        game.display.set_caption('Justified Thief Parody')

        # fill background with black
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
            for event in game.event.get():
                # GUI game loop abstracted to self.check_event() and
                #   subsequent/related functions
                status = self.check_event(event=event)
                if status is not None:
                    return status

            # re-render text-entry box
            # if user_entry is not empty, also re-render that text within box
            if self.game_start:
                self.set_game_start()

            self.render_text_entry_box()
            if self.user_entry != '':
                self.render_user_text_in_box()
            game.display.update()

    def set_game_start(self) -> None:
        if self.is_load:
            load = save_load.LoadGame(
                os.path.join(saves, self.load_name)
            )
            self.scroll.text_in_scroll = load.scroll
            self.set_game_screen()
        else:
            save_load.start_new_game()
            self.handle_game_text(
                init_text=player_location.room.get_room_narration())
        self.game_start = False

    def set_game_screen(self) -> None:
        """
        takes 1 optional parameter: highlighted with a default state of 0
        Returns None

        Renders game screen and calls all component rendering functions
            including: draw_outline(), draw_text_entry_box(),
            draw_scroll_text_box(), & write_exit_button()
        """
        # local vars for draw_outline
        buffer: int = 25
        screen_width: int = self.window_height
        board_width: int = screen_width - (2 * buffer)
        thickness: int = 3

        # background
        background = game.Surface(self.surface.get_size())
        background = background.convert()
        background.fill(self.colors['black'])
        self.surface.blit(background, (0, 0))

        # draw outline
        self.render_outline(buffer, thickness, board_width,
                            self.colors['white'])
        # draw text-entry box
        self.render_text_entry_box()
        # draw entered text box
        self.render_scroll_text_box()
        # write buttons: Exit, Save, View Previous & View Next
        self.render_button(btn_text='Exit', pos=(730, 65))
        self.render_button(btn_text='Save', pos=(730, 35))
        if len(self.scroll.text_in_scroll) > 23 and \
                self.scroll_page != self.scroll.get_max_scroll_page():
            self.render_button(btn_text='View Previous Page', pos=(45, 35))
        if self.scroll_page > 0:
            self.render_button(btn_text='View Next Page', pos=(45, 65))
            self.render_button(btn_text='Back to Current Page', pos=(300, 65))

        # display any scroll text that needs displayed
        self.render_text_in_scroll()

    def render_outline(self, buffer: int, thickness: int,
                       window_width: int, color: tuple) -> None:
        """
        takes 4 parameters: buffer, thickness, window_width (int),
            and color (tuple)
        returns None
        renders the white outline
        """
        outline = Rect(buffer - thickness, buffer - thickness,
                       (window_width + (2 * thickness)),
                       window_width + (2 * thickness))
        game.draw.rect(surface=self.surface, color=color,
                       rect=outline, width=thickness)

    def render_text_entry_box(self) -> None:
        """
        takes no parameters
        returns None
        renders the text-entry box (not the text itself)
        """
        text_entry_box = game.Rect(100, 600, 600, 100)
        game.draw.rect(surface=self.surface, color=self.colors['dark_grey'],
                       rect=text_entry_box)

    def render_scroll_text_box(self) -> None:
        """
        takes no parameters
        returns None
        renders the scroll text box (not the text itself)
        """
        text_entry_box = game.Rect(100, 100, 600, 480)
        game.draw.rect(surface=self.surface, color=self.colors['dark_grey'],
                       rect=text_entry_box)

    def render_button(self, btn_text: str, pos: tuple) -> None:
        """
        takes one parameter: highlighted (int)
        returns None

        Renders the clickable Exit button

        If highlighted == 1: render exit_button in highlighted_grey
        Else: render exit_button in grey
        """
        font = game.font.SysFont('dubai', 20)
        button = font.render(btn_text, True, self.colors['grey'])
        button_highlighted = font.render(btn_text, True,
                                         self.colors['hl_grey'])
        self.surface.blit(button, pos)

        if self.highlighted == btn_text:
            self.surface.blit(button_highlighted, pos)
        else:
            self.surface.blit(button, pos)

    # text-entry citation:
    #   https://www.semicolonworld.com/question/55305/
    #       how-to-create-a-text-input-box-with-pygame
    def handle_text_entry(self, event: game.event) -> str:
        """
        takes two parameters: event (pygame.event), text (str)
        If event.key == 'return' -> add text to self.scroll.text_in_scroll
            and re-render accordingly
        If event.key == 'backspace' -> remove last character in text
        If event.key is anything else, append the char to str text
        return text
        """
        # if user presses 'return', append text entry to
        #   self.scroll.text_in_scroll
        if not self.game_typing:
            if event.key == game.K_RETURN:

                # append to scroll var
                self.scroll.text_in_scroll[-1] += self.user_entry
                self.scroll.text_in_scroll.append('')

                # redraw the scroll text box to 'overwrite' any previously
                #   rendered text
                self.render_scroll_text_box()

                # anytime we want to display text from self.text_in_scroll
                #   we need to ensure it is of appropriate size, and thus need
                #   to call self.scroll.handle_scroll_size()
                self.render_text_in_scroll()
                self.game_typing = True
            elif event.key == game.K_BACKSPACE:
                if self.user_entry != '':
                    self.user_entry = self.user_entry[:-1]
            else:
                self.user_entry += event.unicode

    def render_text_in_scroll(self) -> None:
        """
        takes no parameters
        renders self.text_in_scroll within scroll-text box
        """
        x: int = 110
        y: int = 105
        font = game.font.SysFont('dubai', 20)

        # display text one line at a time
        #   increment 'y' to display each line below the previous
        text_length = len(self.scroll.text_in_scroll)
        if text_length <= 23:
            for text in self.scroll.text_in_scroll:
                text_img = font.render(text, True, self.colors['off_white'])
                self.surface.blit(text_img, (x, y))
                y += 20
        else:
            idx_start = text_length - ((self.scroll_page * 23) + 23)
            if idx_start < 0:
                idx_start = 0
            idx_end = idx_start + 23
            for i in range(idx_start, idx_end):
                text_img = font.render(self.scroll.text_in_scroll[i], True,
                                       self.colors['off_white'])
                self.surface.blit(text_img, (x, y))
                y += 20

    def render_user_text_in_box(self) -> None:
        """
        takes one parameter: user_text (str)
        renders that text within the text-entry box
        """
        font = game.font.SysFont('dubai', 20)
        text_img = font.render(self.user_entry, True, self.colors['off_white'])
        self.surface.blit(text_img, (110, 610))

    def handle_game_text(self, init_text='') -> str:
        if init_text != '':
            game_text = self.parse_game_text(init_text=init_text)
        else:
            game_text = self.parse_game_text()

        self.render_game_text(text_list=game_text)

    def parse_game_text(self, init_text='') -> list:
        """
        takes one parameter: text (str)
        returns a list of strings in the form that is displayable:
            ie. fewer than 75 chars per line, split at space chars, and with
            newline chars accounted for
        """

        # TESTING
        # INTEGRATE WITH TEXT-PARSING, ETC
        # sample_text to be replaced by function parameter 'text'
        # sample_text = 'This is text for testing.. \n' \
        #               'I wanted to practice this "typing" effect \n' \
        #               'as well as handling newline chars..'
        sample_text2 = 'This is a very long sentence that will be used to ' \
                       'test that a string will wrap around once it gets a ' \
                       'certain length as opposed to overflowing off-screen' \
                       '\nnote the newline chars accounted for\nit also ' \
                       'accounts for where the last space char exists so ' \
                       'words do not get split in the middle'

        caps = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                'Y', 'Z']

        text_list = []
        max_chars = 75

        if init_text != '':
            game_text = init_text
        else:
            game_text = get_next_narration(self.user_entry)

        if game_text.lower().startswith('you go') \
            or game_text.lower().startswith('you look around'):
            game_text += '\n\n' + player_location.room.get_room_narration()

        if '_game_over_' in game_text:
            idx = game_text.index('_game_over_')
            game_text = game_text[:idx]
            self.game_over = True
        elif '_game_win_' in game_text:
            idx = game_text.index('_game_win_')
            game_text = game_text[:idx]
            self.game_win = True

        # check for \n as they don't play nicely with pygame rendering
        # if \n, split text into a list of single lines to be displayed
        if len(game_text) > max_chars:
            strings_count = 1 + len(game_text) // max_chars + \
                            game_text.count('\n')
            split_index: list = [0]

            parse_done = False
            x = 0

            while not parse_done:
                max_chars = 73

                # for a string up to length max_chars, find the last occurrence
                #   of a ' ' char. This is where we will split the string so
                #   the splitting does not occur in the middle of words
                if (max_chars + split_index[x]) >= len(game_text):
                    y = len(game_text)
                    w = y - split_index[x]

                    for char in game_text[split_index[x]:y]:
                        if char in caps:
                            max_chars -= 0.8

                    max_chars = ceil(max_chars)

                    if w > max_chars:
                        y = split_index[x] + max_chars
                        split_index.append(game_text[split_index[x]:y].
                                           rindex(' ') + split_index[x] + 1)

                        to_list = game_text[split_index[x]:split_index[x + 1]]
                    else:
                        split_index.append(y)
                        to_list = game_text[split_index[x]:split_index[x + 1]]
                        if '\\n' in to_list:
                            nl_idx = to_list.index('\\n')
                            split_index[x + 1] = nl_idx + split_index[x]
                            split_index.append(y)
                            game_text = game_text[:split_index[x + 1]] + \
                                        game_text[(split_index[x + 1] + 2):]
                            to_list = game_text[
                                      split_index[x]:split_index[x + 1]]
                        if '\n' in to_list:
                            nl_idx = to_list.index('\n')
                            split_index[x + 1] = nl_idx + split_index[x]
                            split_index.append(y)
                            game_text = game_text[:split_index[x + 1]] + \
                                        game_text[(split_index[x + 1] + 1):]
                            to_list = game_text[
                                      split_index[x]:split_index[x + 1]]
                        else:
                            parse_done = True

                else:
                    y = split_index[x] + max_chars

                    temp = 0
                    for char in game_text[split_index[x]:y]:
                        if char in caps:
                            max_chars -= 0.75
                            temp += 0.75

                    max_chars = ceil(max_chars)

                    if temp > 0:
                        y = split_index[x] + max_chars

                    split_index.append(game_text[split_index[x]:y].
                                       rindex(' ') + split_index[x] + 1)
                    to_list = game_text[split_index[x]:split_index[x + 1]]
                if '\\n' in to_list:
                    nl_idx = to_list.index('\\n')
                    split_index[x + 1] = nl_idx + split_index[x]
                    game_text = game_text[:split_index[x + 1]] + \
                                game_text[(split_index[x + 1] + 2):]
                    to_list = game_text[split_index[x]:split_index[x + 1]]
                if '\n' in to_list:
                    nl_idx = to_list.index('\n')
                    split_index[x + 1] = nl_idx + split_index[x]
                    game_text = game_text[:split_index[x + 1]] + \
                                game_text[(split_index[x + 1] + 1):]
                    to_list = game_text[split_index[x]:split_index[x + 1]]

                text_list.append(to_list)
                x += 1
        else:
            no_newline = True
            for char in game_text:
                if char == '\n':
                    no_newline = False
            if no_newline:
                text_list.append(game_text)
            else:
                split_index: list = [0, len(game_text)]
                parse_done = False
                x = 0
                y = len(game_text)
                to_list = game_text
                while not parse_done:
                    if '\n' in to_list:
                        nl_idx = to_list.index('\n')
                        split_index[x + 1] = nl_idx + split_index[x]
                        split_index.append(y)
                        game_text = game_text[:split_index[x + 1]] + \
                                    game_text[(split_index[x + 1] + 1):]
                        to_list = game_text[split_index[x]:split_index[x+1]]
                    elif '\\n' in to_list:
                        nl_idx = to_list.index('\\n')
                        split_index[x + 1] = nl_idx + split_index[x]
                        split_index.append(y)
                        game_text = game_text[:split_index[x + 1]] + \
                                    game_text[(split_index[x + 1] + 2):]
                        to_list = game_text[split_index[x]:split_index[x+1]]
                    else:
                        to_list = game_text[split_index[x]:split_index[x+1]]
                        parse_done = True

                    text_list.append(to_list)
                    x += 1

        return text_list

    def render_game_text(self, text_list: list) -> None:
        """
        takes one parameter: text_list (list<str>)
        renders text_list line by line to text scroll
        """
        wait_val = 3
        for line in text_list:
            self.scroll.text_in_scroll.append('')

            # renders line char-by-char to emulate typing onto screen
            for char in line:
                self.scroll.text_in_scroll[-1] += char

                # redraw the scroll text box to 'overwrite' any previously
                #   rendered text
                self.render_scroll_text_box()

                # anytime we want to display text from self.text_in_scroll
                #   we need to ensure it is of appropriate size, and thus need
                #   to call self.scroll.handle_scroll_size()
                self.render_text_in_scroll()
                game.display.update()
                game.time.wait(wait_val)
            game.time.wait(wait_val * 2)

        self.scroll.text_in_scroll.append('')
        self.scroll.text_in_scroll.append('>')
        self.render_scroll_text_box()
        self.render_text_in_scroll()
        game.display.update()

        self.user_entry = ''
        self.game_typing = False

    def view_history(self, direction: str):
        """
        takes one parameter: direction (str) which can either be 'prev',
            'next', or 'reset'
        returns None
        """
        if direction == 'prev':
            if self.scroll_page != self.scroll.get_max_scroll_page():
                self.scroll_page += 1

        if direction == 'next':
            if self.scroll_page > 0:
                self.scroll_page -= 1

        if direction == 'reset':
            if self.scroll_page > 0:
                self.scroll_page = 0

        self.set_game_screen()

    def check_event(self, event):
        """
        abstraction of GUI while game loop
        calls one of the following based on game events:
            self.handle_mouse_motion_event()
            self.handle_mouse_click_event()
            self.handle_keydown_event()
        returns None
        """
        if self.game_over:
            return '_game_over_'
        if self.game_win:
            return '_game_win_'

        if event.type == game.QUIT:
            game.quit()
            sys.exit()

        elif event.type == game.MOUSEMOTION:
            self.handle_mouse_motion_event()

        elif event.type == game.MOUSEBUTTONDOWN:
            status = self.handle_mouse_click_event()
            if status == 'main menu':
                return status

        elif event.type == game.KEYDOWN:
            status = self.handle_keydown_event(events=event)
            if status is not None:
                return status

    def handle_mouse_motion_event(self):
        mouse = game.mouse.get_pos()

        if 760 > mouse[0] > 730 and 60 > mouse[1] > 40:
            # highlighted = 1 will render the exit_button as
            #   'highlighted_grey'
            self.highlighted: str = 'Save'
        elif 760 > mouse[0] > 730 and 90 > mouse[1] > 70:
            # highlighted = 1 will render the exit_button as
            #   'highlighted_grey'
            self.highlighted: str = 'Exit'
        elif 195 > mouse[0] > 45 and 60 > mouse[1] > 40:
            self.highlighted: str = 'View Previous Page'
        elif self.scroll_page > 0 and 175 > mouse[0] > 45 and \
                90 > mouse[1] > 70:
            self.highlighted: str = 'View Next Page'
        elif self.scroll_page > 0 and 475 > mouse[0] > 300 and \
                90 > mouse[1] > 70:
            self.highlighted: str = 'Back to Current Page'
        else:
            # only perform re-render if exit_button was previously
            #   highlighted
            if self.highlighted != '':
                self.highlighted: str = ''

        self.set_game_screen()

    def handle_mouse_click_event(self):
        click = game.mouse.get_pressed(3)
        mouse = game.mouse.get_pos()

        if click[0] == 1:
            # if in area of save btn
            if 760 > mouse[0] > 730 and 60 > mouse[1] > 40:
                while 1:
                    save_game: str = save_gui.SaveGUI().main()
                    if save_game == 'back':
                        break
                    elif save_game != 'refresh':
                        save_file_name = save_game
                        new_save = save_load.SaveGame(
                            save_file_name=save_file_name,
                            cur_scroll=self.scroll
                        )
                        print("attempting to save: ", save_file_name)
                        break
                self.set_game_screen()
            # elif in area of exit btn
            elif 760 > mouse[0] > 730 and 90 > mouse[1] > 70:
                return 'main menu'
            # elif in area of View Previous btn
            elif 195 > mouse[0] > 45 and 60 > mouse[1] > 40:
                self.view_history(direction='prev')
            # elif in area of View Next btn
            elif self.scroll_page > 0 and 175 > mouse[0] > 45 and \
                    90 > mouse[1] > 70:
                self.view_history(direction='next')
            # elif in area of Back to Current btn
            elif self.scroll_page > 0 and 475 > mouse[0] > 300 and \
                    90 > mouse[1] > 70:
                self.view_history(direction='reset')

    def handle_keydown_event(self, events):
        if not self.game_typing:
            self.scroll_page = 0
            self.set_game_screen()
            status = self.handle_text_entry(event=events)
            if self.game_over:
                return '_game_over_'
            if self.game_win:
                return '_game_win_'

        if events.key == game.K_RETURN and self.game_typing:
            self.render_text_entry_box()
            game.display.update()
            status = self.handle_game_text()
            if self.game_over:
                return '_game_over_'
            if self.game_win:
                return '_game_win_'
