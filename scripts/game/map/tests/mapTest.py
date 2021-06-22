import unittest
from pygame import display
from scripts.game.map.map import Map
from scripts.game.map.condition import EnumMap
from scripts.game.map.parametersMap import ParametersMap
from pygame import Vector2


class MapTest(unittest.TestCase):
    def setUp(self) -> None:
        name = 'test'
        self.size = (100, 100)
        self.border = Vector2(10, 0)
        self.surface = display.set_mode(self.size)
        self.map = Map(ParametersMap(
            name=name,
            surface=self.surface,
            condition=EnumMap.Player,
            border=self.border,
            size=Vector2(self.size)
        ))

    def test_input_mouse_1(self):
        mouse = Vector2(20, 10)
        a = self.map.check_input(mouse)
        b = True
        self.assertEqual(a, b)

    def test_input_mouse_2(self):
        mouse = Vector2(2, 10)
        a = self.map.check_input(mouse)
        b = False
        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
