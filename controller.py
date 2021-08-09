import pygame as game
import sys
from gui import main_menu_gui, game_end
import game_gui
import load_gui
from time import sleep
import os

base_dir = os.path.dirname(__file__)
audio = os.path.join(base_dir, r"audio")


class IntroMusic:
    def __init__(self):
        game.mixer.init()
        self.main_theme = game.mixer.Sound(
            os.path.join(audio, "mainTheme3.wav")
        )

    def start_music(self):
        game.mixer.Sound.play(self.main_theme, loops=-1)

    def stop_music(self):
        self.main_theme.fadeout(3000)


def controller() -> None:
    """
    Takes no parameters,
    Returns None

    To be executed upon app start

    Listens for returns from function calls and directs activity
    accordingly
    """
    main_return = main_menu_gui.MainMenuGUI().main()

    # from GameGUI:
    #   if main_return is 'new game' -> call start_game() to
    #       run new game
    #   elif main_return is 'exit' -> quit game
    #   elif main_return is 'load game' -> load game
    #   else -> rerun mainMenu
    if main_return == 'new game':
        music.stop_music()
        sleep(3)
        start_game()
    elif main_return == 'exit':
        music.stop_music()
        game.quit()
        sys.exit()
    elif main_return == 'load game':
        load_game()


def start_game(is_load: bool = False, load_name: str = '') -> None:
    """
    Starts a new game by instantiating a GameGUI() object and calling main()
    """
    game_return = game_gui.GameGUI(is_load=is_load, load_name=load_name).main()

    # 'main menu' is returned upon clicking the exit_button in game_gui
    if game_return == "main menu":
        music.start_music()
        controller()
    elif game_return == "_game_over_":
        end("_game_over_")
    elif game_return == "_game_win_":
        end("_game_win_")


def load_game() -> None:
    """
    Instantiates a LoadGameGUI() object and calls main()

    LoadGameGUI() listens for MOUSEMOTION and MOUSEBUTTONDOWN events
        to detect which game to load
    """

    # this will eventually return something like a save_id to load a formally
    # saved state
    load = load_gui.LoadGameGUI().main()
    if load == 'back':
        controller()
    else:
        print("loading -> ", load)
        music.stop_music()
        sleep(3)
        start_game(is_load=True, load_name=load)


def end(status) -> None:
    music.start_music()
    end_return = game_end.GameEnd(status).main()
    if end_return == 'load':
        load_game()
    else:
        print(end_return)
        controller()


music = IntroMusic()
music.start_music()

controller()
