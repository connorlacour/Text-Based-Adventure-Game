import pygame as game
import sys
import game_gui
import main_menu_gui
import load_gui
from time import sleep


class IntroMusic:
    def __init__(self):
        game.mixer.init()
        self.main_theme = game.mixer.Sound(r"..\audio\mainTheme3.wav")

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
        print('okay.. exiting..')
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
    if game_return == "save game":
        save_game()


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
        music.start_music()
        controller()
    else:
        print("loading -> ", load)
        music.stop_music()
        sleep(3)
        start_game(is_load=True, load_name=load)


def save_game() -> None:
    """
    Instantiates a SaveGameGUI() object and calls main()
    """
    print('saving game..')
    controller()


music = IntroMusic()
music.start_music()

controller()
