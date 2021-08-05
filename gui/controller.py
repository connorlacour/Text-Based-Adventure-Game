import pygame as game
import sys
import game_gui
import main_menu_gui
import load_gui


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
        print('starting new game\none moment..')
        start_new_game()
    elif main_return == 'exit':
        print('okay.. exiting..')
        game.quit()
        sys.exit()
    elif main_return == 'load game':
        load_game()


def start_new_game() -> None:
    """
    Starts a new game by instantiating a GameGUI() object and calling main()
    """
    game_return = game_gui.GameGUI().main()

    # 'main menu' is returned upon clicking the exit_button in game_gui
    if game_return == "main menu":
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

    if load == 'load':
        start_new_game()
    elif load == 'back':
        controller()


def save_game() -> None:
    """
    Instantiates a SaveGameGUI() object and calls main()
    """
    print('saving game..')
    controller()


controller()
