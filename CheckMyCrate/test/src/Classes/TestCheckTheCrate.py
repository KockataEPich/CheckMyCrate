import unittest
import src.Classes.CheckTheCrate as CTC
import os

class TestCheckTheCrate(unittest.TestCase):
    def test_checkTheCrate(self):
        self.assertFalse(CTC.checkTheCrate("test/sample/", "test/profile_library/ro_crate_1.1_basic.json"))

if __name__ == '__main__':
    unittest.main()