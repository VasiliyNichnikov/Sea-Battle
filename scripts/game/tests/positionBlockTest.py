import unittest
from pygame import Vector2, Rect
from scripts.game.block.positionBlock import PositionBlock


class PositionBlockTest(unittest.TestCase):
    def setUp(self) -> None:
        self.number_block = Vector2(5, 5)
        self.border = Vector2(10, 10)
        self.block_size = 40
        self.position_block = PositionBlock(self.number_block, self.border, self.block_size)

    def test_rect(self):
        position = self.position_block.position
        a = self.position_block.rect
        b = Rect(position.x, position.y, self.block_size, self.block_size)
        self.assertEqual(a, b)

    def test_position(self):
        a = self.position_block.position
        b = Vector2(self.number_block.x * self.block_size + self.border.x,
                    self.number_block.y * self.block_size + self.border.y)
        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
