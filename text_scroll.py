class Scroll:
    def __init__(self, test: int = 0):
        if test == 0:
            self.text_in_scroll = []
        else:
            self.text_in_scroll = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                                   'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                                   's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '',
                                   '>']

    def display_text_in_scroll(self) -> list:
        """
        returns text_in_scroll
        """
        txt_len = len(self.text_in_scroll)
        display_text = self.text_in_scroll[(txt_len - 20):txt_len]

        return display_text

    def clear_text_in_scroll(self) -> None:
        """
        clears text_in_scroll
        """
        self.text_in_scroll = []

    def get_max_scroll_page(self) -> int:
        if len(self.text_in_scroll) % 23 == 0:
            max_page = (len(self.text_in_scroll) // 23) - 1
        else:
            max_page = len(self.text_in_scroll) // 23
        return max_page
