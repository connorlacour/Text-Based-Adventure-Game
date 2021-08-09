class Colors:
    def __init__(self):
        self.colors = {}
        self.init_colors()

    def init_colors(self):
        self.colors['black']: tuple = (0, 0, 5)
        self.colors['white']: tuple = (250, 250, 250)
        self.colors['dark_grey']: tuple = (30, 30, 30)
        self.colors['darker_grey']: tuple = (20, 20, 20)
        self.colors['hl_grey']: tuple = (200, 200, 225)
        self.colors['med_grey']: tuple = (60, 60, 60)
        self.colors['hl_dark_grey']: tuple = (135, 135, 135)
        self.colors['grey']: tuple = (100, 100, 100)
        self.colors['off_white']: tuple = (220, 220, 220)
        self.colors['offer_white']: tuple = (200, 200, 200)

    def add_color(self, name, color_val) -> None:
        self.colors[name]: tuple = color_val
        return

    def get_colors(self) -> dict:
        return self.colors

