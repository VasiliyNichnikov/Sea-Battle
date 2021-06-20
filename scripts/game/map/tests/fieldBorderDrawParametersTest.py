import unittest
from pygame import Rect
from scripts.game.map.fieldBorderDrawParameters import FieldBorderDrawParameters


class FieldBorderDrawParametersTest(unittest.TestCase):
    def setUp(self) -> None:
        self.BLACK = (0, 0, 0)
        self.rect = Rect(5, 5, 5, 5)
        self.field_border_draw_parameters = FieldBorderDrawParameters(self.rect, self.BLACK)

    def test_position(self):
        a = self.field_border_draw_parameters.position
        b = self.rect
        self.assertEqual(a, b)

    def test_color(self):
        a = self.field_border_draw_parameters.color
        b = self.BLACK
        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
