import pygame as game
from pygame.locals import *
import sys
import text_scroll as scroll
import colors


class GameGUI:
    def __init__(self):
        self.window_height = 800
        self.surface = game.display.set_mode((800, 800))

        # to test scrolling (ie. initialize with several too many elements),
        #   self.scroll = scroll.Scroll(1)
        # else:
        #   self.scroll = scroll.Scroll()
        self.scroll = scroll.Scroll(1)
        self.colors: dict = colors.Colors().get_colors()
        self.game_typing = False
        self.user_typing = False

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
        game.display.set_caption('GAME TITLE')

        # fill background with brown
        background = game.Surface(self.surface.get_size())
        background = background.convert()
        background.fill(self.colors['black'])

        # Blit background to the screen
        self.surface.blit(background, (0, 0))
        game.display.flip()
        self.set_game_screen()

        # initialize user_entry and highlighted to be used in main() while loop
        user_entry: str = ''
        highlighted: int = 0

        # while 1 loop maintains display updates and should only terminate
        #   upon game ending
        while 1:
            # constant check for game.QUIT
            for events in game.event.get():
                if events.type == game.QUIT:
                    game.quit()
                    sys.exit()

                elif events.type == game.MOUSEMOTION:
                    mouse = game.mouse.get_pos()

                    if 760 > mouse[0] > 730 and 60 > mouse[1] > 40:
                        # highlighted = 1 will render the exit_button as
                        #   'highlighted_grey'
                        highlighted: int = 1

                        # entire game_screen must be re-rendered, so we must
                        #   ensure that the scroll text and all other
                        #   components are appropriately maintained
                        self.set_game_screen(highlighted)
                        self.draw_scroll_text_box()
                        self.scroll.handle_scroll_size()
                        self.display_text_in_scroll()
                    else:
                        # only perform re-render if exit_button was previously
                        #   highlighted
                        if highlighted == 1:
                            highlighted: int = 0

                            # entire game_screen must be re-rendered, so we
                            #   must ensure that the scroll text and all other
                            #   components are appropriately maintained
                            self.set_game_screen(highlighted)
                            self.draw_scroll_text_box()
                            self.scroll.handle_scroll_size()
                            self.display_text_in_scroll()

                elif events.type == game.MOUSEBUTTONDOWN:
                    click = game.mouse.get_pressed(3)
                    mouse = game.mouse.get_pos()

                    # if in area of exit_button
                    if 760 > mouse[0] > 730 and 60 > mouse[1] > 40:
                        if click[0] == 1:
                            return 'main menu'

                # if user is typing, handle text-entry by calling
                #   self.handle_text_entry()
                elif events.type == game.KEYDOWN:
                    if not self.game_typing:
                        user_entry = self.handle_text_entry(
                            event=events, text=user_entry)
                    if events.key == game.K_RETURN and self.game_typing:
                        self.draw_text_entry_box()
                        game.display.update()
                        self.handle_game_text()

            # re-render text-entry box
            # if user_entry is not empty, also re-render that text within box
            self.draw_text_entry_box()
            if user_entry != '':
                self.display_user_text_in_box(user_text=user_entry)
            game.display.update()

    def set_game_screen(self, highlighted: int = 0) -> None:
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
        board_width: int = screen_width - (2*buffer)
        thickness: int = 3

        # draw outline
        self.draw_outline(buffer, thickness, board_width, self.colors['white'])
        # draw text-entry box
        self.draw_text_entry_box()
        # draw entered text box
        self.draw_scroll_text_box()
        # write exit button
        self.write_exit_button(highlighted=highlighted)

        # display any scroll text that needs displayed
        # THIS IS FOR TESTING
        self.scroll.handle_scroll_size()
        self.display_text_in_scroll()
        # END TESTING SEGMENT

    def draw_outline(self, buffer: int, thickness: int,
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

    def draw_text_entry_box(self) -> None:
        """
        takes no parameters
        returns None

        renders the text-entry box (not the text itself)
        """
        text_entry_box = game.Rect(100, 600, 600, 100)
        game.draw.rect(surface=self.surface, color=self.colors['dark_grey'],
                       rect=text_entry_box)

    def draw_scroll_text_box(self) -> None:
        """
        takes no parameters
        returns None

        renders the scroll text box (not the text itself)
        """
        text_entry_box = game.Rect(100, 100, 600, 480)
        game.draw.rect(surface=self.surface, color=self.colors['dark_grey'],
                       rect=text_entry_box)

    def write_exit_button(self, highlighted: int = 0) -> None:
        """
        takes one parameter: highlighted (int)
        returns None

        Renders the clickable Exit button

        If highlighted == 1: render exit_button in highlighted_grey
        Else: render exit_button in grey
        """
        font = game.font.SysFont('dubai', 20)
        exit_button = font.render('Exit', True, self.colors['grey'])
        exit_button_highlighted = font.render('Exit', True,
                                              self.colors['hl_grey'])
        self.surface.blit(exit_button, (730, 35))

        if highlighted == 1:
            self.surface.blit(exit_button_highlighted, (730, 35))
        else:
            self.surface.blit(exit_button, (730, 35))

    # text-entry citation:
    #   https://www.semicolonworld.com/question/55305/
    #       how-to-create-a-text-input-box-with-pygame
    def handle_text_entry(self, event: game.event, text: str) -> str:
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
                self.scroll.text_in_scroll.append(text)

                # redraw the scroll text box to 'overwrite' any previously
                #   rendered text
                self.draw_scroll_text_box()

                # anytime we want to display text from self.text_in_scroll
                #   we need to ensure it is of appropriate size, and thus need
                #   to call self.scroll.handle_scroll_size()
                self.scroll.handle_scroll_size()
                self.display_text_in_scroll()
                self.game_typing = True
                return ''
            elif event.key == game.K_BACKSPACE:
                if text != '':
                    text = text[:-1]
            else:
                text += event.unicode

        return text

    def display_text_in_scroll(self) -> None:
        """
        takes no parameters
        renders self.text_in_scroll within scroll-text box
        """
        x: int = 110
        y: int = 105
        font = game.font.SysFont('dubai', 20)

        # display text one line at a time
        #   increment 'y' to display each line below the previous
        for text in self.scroll.text_in_scroll:
            text_img = font.render(text, True, self.colors['off_white'])
            self.surface.blit(text_img, (x, y))
            y += 20

    def display_user_text_in_box(self, user_text: str) -> None:
        """
        takes one parameter: user_text (str)
        renders that text within the text-entry box
        """
        font = game.font.SysFont('dubai', 20)
        text_img = font.render(user_text, True, self.colors['off_white'])
        self.surface.blit(text_img, (110, 610))

    def handle_game_text(self) -> None:
        game_text = self.load_game_text()
        self.display_game_text(text_list=game_text)
        return

    def load_game_text(self, text='') -> list:
        # INTEGRATE WITH TEXT-PARSING, ETC
        # sample_text to be replaced by function parameter 'text'
        sample_text = 'This is text for testing.. \n' \
                      'I wanted to practice this "typing" effect \n' \
                      'as well as handling newline chars..'
        text_list = []

        # check for \n as they don't play nicely with pygame rendering
        # if \n, split text into a list of single lines to be displayed
        if '\n' in sample_text:
            print("true")
            text_list = sample_text.split('\n')
        else:
            text_list.append(sample_text)
        return text_list

    def display_game_text(self, text_list: list) -> None:
        wait_val = 40

        for line in text_list:
            self.scroll.text_in_scroll.append('')
            for char in line:
                self.scroll.text_in_scroll[-1] += char

                # redraw the scroll text box to 'overwrite' any previously
                #   rendered text
                self.draw_scroll_text_box()

                # anytime we want to display text from self.text_in_scroll
                #   we need to ensure it is of appropriate size, and thus need
                #   to call self.scroll.handle_scroll_size()
                self.scroll.handle_scroll_size()
                self.display_text_in_scroll()
                game.display.update()
                game.time.wait(wait_val)
        self.user_typing = True
        self.game_typing = False
        return True

