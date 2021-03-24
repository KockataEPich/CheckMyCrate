import unittest
from src.Classes.ProfileValidation import checkProfile

class TestProfileValidation(unittest.TestCase):
    def testCorrectProfile(self):
        self.assertTrue(checkProfile("test/profile_library/ro_crate_1.1_basic.json"))

    def testNonExistentProfile(self):
        self.assertFalse(checkProfile("non_existent_file"))

    def testMissingExpectedType(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile3.json"))

    def testWrongExpectedTypeInProfile(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile1.json"))

    def testMissingPropertiesEntity(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile2.json"))

    def testWrongPropertiesEntity(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile4.json"))

    def testWrongMinimalEntity(self):
         self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile5.json"))

    def testWrongRecommendedEntity(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile6.json"))

    def testWrongOptionalEntity(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile7.json"))

    def testMissingMinimalEntity(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile8.json"))

    def testFourthItemInProperties(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile9.json"))

    def testIncorrectNumberOfElementsInItem(self):         
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile10.json"))

    def testMissingIdFieldInItem(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile11.json"))

    def testSixthKeywordInItem(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile12.json"))

    def testInvalidCardinalityValue(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile13.json"))

    def testThirdGlobalEntity(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile14.json"))

    def testWrongTypeKeyword(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile15.json"))

    def testWrongDescriptionKeyword(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile16.json"))

    def testWrongCardinalityKeyword(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile17.json"))

    def testNonUniqueId(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile18.json"))

    def testInvalidJsonProfile(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile19.json"))

    def testWrongValueKeyword(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile20.json"))
      
    def testWrongValueValue(self):
        self.assertFalse(checkProfile("test/profile_library/wrong_profiles/wrongProfile21.json"))

if __name__ == '__main__':
    unittest.main()
