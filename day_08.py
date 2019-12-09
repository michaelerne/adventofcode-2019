from functools import partial
from os.path import basename, splitext
from typing import List

from PIL import Image  # type: ignore
import pytesseract  # type: ignore

from lib import solve

DAY: int = int(splitext(basename(__file__))[0].split('_')[1])
SOLVE = partial(solve, DAY)

HEIGHT, WIDTH = 6, 25
PICTURE_SIZE = HEIGHT * WIDTH
TRANSPARENT = 2
BLACK = 1
WHITE = 0


def part_a(data: List[List[int]]) -> int:
    fewest_zeros = min(data, key=lambda layer: layer.count(0))

    return fewest_zeros.count(1) * fewest_zeros.count(2)


# pylint: disable=C0103
def get_pixel(data, x, y):
    offset = (y * WIDTH) + x
    pixel = data[0][offset]

    if pixel == TRANSPARENT:
        return get_pixel(data[1:], x, y)
    return pixel


def part_b(data: List[int]) -> str:
    # start with a black image
    image = Image.new('RGB', (WIDTH + 10, HEIGHT + 10), "black")
    pixels = image.load()

    # paint in the pixels
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            color = get_pixel(data, x, y) * 255
            pixels[x + 5, y + 5] = (color, color, color)

    # resize and blur the image
    image = image.resize((WIDTH * 10, HEIGHT * 10), Image.BILINEAR)

    # OCR
    text = pytesseract.image_to_string(image)

    return text


def parse(data: str) -> List[List[int]]:
    data_int = [int(x) for x in data]
    layer_starts = range(0, len(data_int), PICTURE_SIZE)
    layers = [data_int[i:i + PICTURE_SIZE] for i in layer_starts]
    return layers


if __name__ == "__main__":
    SOLVE(part_a, parse, False)

    SOLVE(part_b, parse, False)
