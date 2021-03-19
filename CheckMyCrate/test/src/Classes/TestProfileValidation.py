import unittest
import src.Classes.ProfileValidation as PV

class TestProfileValidation(unittest.TestCase):
    def testPorifleValidation(self):
        self.assertTrue(PV.checkProfile("test/profile_library/ro_crate_1.1_basic.json"))
        self.assertFalse(PV.checkProfile("non_existent_file"))

        self.assertFalse(PV.checkProfile("test/profile_library/wrong_profiles/wrongProfile1.json"))
        self.assertFalse(PV.checkProfile("test/profile_library/wrong_profiles/wrongProfile2.json"))
        self.assertFalse(PV.checkProfile("test/profile_library/wrong_profiles/wrongProfile3.json"))
        self.assertFalse(PV.checkProfile("test/profile_library/wrong_profiles/wrongProfile4.json"))
        self.assertFalse(PV.checkProfile("test/profile_library/wrong_profiles/wrongProfile5.json"))
        self.assertFalse(PV.checkProfile("test/profile_library/wrong_profiles/wrongProfile6.json"))
        self.assertFalse(PV.checkProfile("test/profile_library/wrong_profiles/wrongProfile7.json"))
        self.assertFalse(PV.checkProfile("test/profile_library/wrong_profiles/wrongProfile8.json"))
        self.assertFalse(PV.checkProfile("test/profile_library/wrong_profiles/wrongProfile9.json"))
        self.assertFalse(PV.checkProfile("test/profile_library/wrong_profiles/wrongProfile10.json"))
        self.assertFalse(PV.checkProfile("test/profile_library/wrong_profiles/wrongProfile11.json"))
        self.assertFalse(PV.checkProfile("test/profile_library/wrong_profiles/wrongProfile12.json"))
        self.assertFalse(PV.checkProfile("test/profile_library/wrong_profiles/wrongProfile13.json"))
        self.assertFalse(PV.checkProfile("test/profile_library/wrong_profiles/wrongProfile14.json"))
        self.assertFalse(PV.checkProfile("test/profile_library/wrong_profiles/wrongProfile15.json"))
        self.assertFalse(PV.checkProfile("test/profile_library/wrong_profiles/wrongProfile16.json"))
        self.assertFalse(PV.checkProfile("test/profile_library/wrong_profiles/wrongProfile17.json"))
      

if __name__ == '__main__':
    unittest.main()
