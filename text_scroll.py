class Scroll:
    def __init__(self, test: int = 0):
        if test == 0:
            self.text_in_scroll = []
        else:
            self.text_in_scroll = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                                   'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                                   's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    def get_text_in_scroll(self) -> list:
        """
        returns text_in_scroll
        """
        return self.text_in_scroll

    def clear_text_in_scroll(self) -> None:
        """
        clears text_in_scroll
        """
        self.text_in_scroll = []

    def handle_scroll_size(self):
        """
        if text_in_scroll exceeds length 23, handle_scroll_size will pop
        elements off the list until length <= 23
        """
        if len(self.text_in_scroll) > 23:
            while len(self.text_in_scroll) > 23:
                self.text_in_scroll.pop(0)
