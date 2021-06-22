import unittest
from pygame import Vector2, display, Rect
from scripts.game.map.parametersMap import ParametersMap
from scripts.game.map.condition import EnumMap
from scripts.colorsAndMainParameters import number_blocks, block_size


class ParametersMapTest(unittest.TestCase):
    def setUp(self) -> None:
        self.name = 'test'
        self.surface = display.set_mode((10, 10))
        self.size = Vector2(10, 10)
        self.border = Vector2(5, 5)
        self.condition = EnumMap.Player
        self.parameters_map = ParametersMap(self.name, self.surface, self.condition, self.size, self.border)

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
        b = Rect(self.border.x, self.border.y, self.size.x, self.size.y)
        self.assertEqual(a, b)

    def test_condition(self):
        a = self.parameters_map.condition
        b = self.condition
        self.assertEqual(a, b)

    def test_size(self):
        a = self.parameters_map.size
        b = self.size
        self.assertEqual(a, b)

if __name__ == '__main__':
    unittest.main()
