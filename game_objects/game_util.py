import os


def print_warning(str):
    print(f"Warning! {str}")

def debug_print(str):
    print(str)

def get_file_name(filename, dir_name):
    return os.path.join(dir_name, f'{filename}')

def warning_room_not_found(room):
    if room is None:
        print_warning(f"{str} not found in room list")
        return False
    return True


def warning_item_not_found(item):
    if item is None:
        print_warning(f"{str} not found in item list")
