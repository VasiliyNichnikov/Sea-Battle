import unittest
from scripts.game.block.condition import EnumBlock
from scripts.game.block.conditionBlock import ConditionBlock


class ConditionBlockTest(unittest.TestCase):
    def setUp(self) -> None:
        self.condition_block = ConditionBlock()

    def test_change_to_lock(self):
        self.condition_block.change_to_lock()
        a = self.condition_block.condition
        b = EnumBlock.Lock
        self.assertEqual(a, b)

    def test_change_to_empty(self):
        self.condition_block.change_to_empty()
        a = self.condition_block.condition
        b = EnumBlock.Empty
        self.assertEqual(a, b)

    def test_change_to_hit(self):
        self.condition_block.change_to_hit()
        a = self.condition_block.condition
        b = EnumBlock.Hit
        self.assertEqual(a, b)

    def test_change_to_miss(self):
        self.condition_block.change_to_miss()
        a = self.condition_block.condition
        b = EnumBlock.Miss
        self.assertEqual(a, b)

    def test_change_to_selected(self):
        self.condition_block.change_to_selected()
        a = self.condition_block.condition
        b = EnumBlock.Selected
        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
