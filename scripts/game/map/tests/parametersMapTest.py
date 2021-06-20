import unittest
from pygame import Vector2, display, Rect
from scripts.game.map.parametersMap import ParametersMap
from scripts.colorsAndMainParameters import number_blocks, block_size


class ParametersMapTest(unittest.TestCase):
    def setUp(self) -> None:
        self.surface = display.set_mode((10, 10))
        self.name = 'test'
        self.border = Vector2(10, 10)
        self.parameters_map = ParametersMap(self.surface, self.name, self.border)

    def test_surface(self):
        a = self.parameters_map.surface
        b = self.surface
        self.assertEqual(a, b)

    def test_name(self):
        a = self.parameters_map.name
        b = self.name
        self.assertEqual(a, b)

    def test_border(self):
        a = self.parameters_map.border
        b = self.border
        self.assertEqual(a, b)

    def test_blocks(self):
        a = self.parameters_map.blocks
        b = [[object] * 10] * 10
        self.assertEqual(a, b)

    def test_rect(self):
        a = self.parameters_map.rect
        b = Rect(self.border.x, self.border.y, number_blocks * block_size, number_blocks * block_size)
        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
