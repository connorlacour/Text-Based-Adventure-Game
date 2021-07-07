import pygame as game
import sys
import game_gui
import main_menu_gui


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
    #   elif main_return is 'options' -> call options() to
    #       run options menu ******* WRITE *******
    #   else -> rerun mainMenu
    if main_return == 'new game':
        print('starting new game\none moment..')
        start_new_game()
    elif main_return == 'exit':
        print('okay.. exiting..')
        game.quit()
        sys.exit()
    elif main_return == 'options':
        print('opening options..')


def game_menu() -> None:
    """
    To be implemented as an in-game menu
    Should allow exit, load, save
    """
    pass


def start_new_game() -> None:
    """
    Starts a new game by instantiating a GameGUI() object and calling main()
    """
    game_return = game_gui.GameGUI().main()

    # 'main menu' is returned upon clicking the exit_button in game_gui
    if game_return == "main menu":
        controller()


controller()
