import unittest
from pygame import Vector2
from pygame import display
from scripts.game.block.conditionBlock import ConditionBlock
from scripts.game.block.parametersBlock import ParametersBlock


class ParametersBlockTest(unittest.TestCase):
    def setUp(self) -> None:
        self.surface = display.set_mode((100, 100))
        self.block_size = 40
        self.number_block = Vector2(5, 5)
        self.border = Vector2(10, 10)
        self.parameters_block = ParametersBlock(self.surface, self.number_block, self.border, self.block_size)

    def test_surface(self):
        a = self.parameters_block.surface
        b = self.surface
        self.assertEqual(a, b)

    def test_block_size(self):
        a = self.parameters_block.block_size
        b = self.block_size
        self.assertEqual(a, b)

    def test_position_block(self):
        a = self.parameters_block.number_block
        b = self.number_block
        self.assertEqual(a, b)

    def test_condition_block(self):
        a = self.parameters_block.condition_block
        b = ConditionBlock()
        self.assertEqual(type(a), type(b))


if __name__ == '__main__':
    unittest.main()
