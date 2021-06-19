import unittest
from pygame import Vector2
from scripts.game2.block.pointsPerimeter import PointsPerimeter


class PointsPerimeterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.pos = Vector2(10, 10)
        self.block_size = 40
        self.points_perimeter = PointsPerimeter(self.pos, self.block_size)

    def test_get_point_left_up(self):
        a = self.points_perimeter.pos_left_up
        b = Vector2(self.pos.x, self.pos.y + self.block_size)
        self.assertEqual(a, b)

    def test_get_point_left_down(self):
        a = self.points_perimeter.pos_left_down
        b = self.pos
        self.assertEqual(a, b)

    def test_get_point_right_up(self):
        a = self.points_perimeter.pos_right_up
        b = Vector2(self.pos.x + self.block_size, self.pos.y + self.block_size)
        self.assertEqual(a, b)

    def test_get_point_right_down(self):
        a = self.points_perimeter.pos_right_down
        b = Vector2(self.pos.x + self.block_size, self.pos.y)
        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
