import unittest
import src.Classes.CheckTheCrate as CTC
import os

class TestCheckTheCrate(unittest.TestCase):
    def testCorrect(self):
        self.assertTrue(CTC.checkTheCrate("test/sample/", "test/profile_library/modified_profiles/smaller_profile.json", False, False))

    def testInCorrect(self):
        self.assertFalse(CTC.checkTheCrate("test/sample/", "test/profile_library/ro_crate_1.1_basic.json", False, False))

    def testIncorrectNonMinimum(self):
        self.assertFalse(CTC.checkTheCrate("test/sample/", "test/profile_library/modified_profiles/smaller_profile2.json", False, False))

    def testIncorrectNonMinimum2(self):
        self.assertFalse(CTC.checkTheCrate("test/sample/", "test/profile_library/modified_profiles/smaller_profile3.json", False, False)) 

if __name__ == '__main__':
    unittest.main()
