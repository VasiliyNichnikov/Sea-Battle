class ParametersMap:
    def __init__(self):
        self.surface = surface
        self.name = name
        self.border = None
        self.list_blocks = []
        self.rect = pygame.Rect(self.border_x, self.border_y, block_size * number_blocks, block_size * number_blocks)