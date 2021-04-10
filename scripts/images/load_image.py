from pygame.image import load
from pygame.transform import scale


def load_image(path, width=0, height=0, proportionately=True):
    image = load(path)
    if width != 0 and height != 0 and proportionately:
        image_size_x, image_size_y = image.get_width(), image.get_height()
        ratio = min(float(width) / image_size_x, float(height) / image_size_y)
        width = int(image_size_x * ratio)
        height = int(image_size_y * ratio)

    if width == 0:
        width = image.get_width()
    if height == 0:
        height = image.get_height()

    image = scale(image, (width, height))
    return image
