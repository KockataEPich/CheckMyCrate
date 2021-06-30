import unittest
from src.Classes.ProfileValidation import validateProfileJSONFileAndReturnTheDataObject

class TestProfileValidation(unittest.TestCase):
    def testCorrectProfile(self):
        validateProfileJSONFileAndReturnTheDataObject("test/profile_library/template_profile.json")

    def testNonExistentProfile(self):
        with self.assertRaises(ValueError):
            validateProfileJSONFileAndReturnTheDataObject("non_existent_file")

    def testMarginalityNotExisting(self):
        with self.assertRaises(ValueError):
            validateProfileJSONFileAndReturnTheDataObject("test/profile_library/wrong_profiles/MarginalityNotExisting.json")

    def testMatchPatternWithoutValue(self):
        with self.assertRaises(ValueError):
            validateProfileJSONFileAndReturnTheDataObject("test/profile_library/wrong_profiles/MatchPatternWithoutValue.json")

    def testNoItems(self):
        with self.assertRaises(ValueError):
            validateProfileJSONFileAndReturnTheDataObject("test/profile_library/wrong_profiles/NoItems.json")

    def testNotCorrectJSON(self):
        with self.assertRaises(ValueError):
            validateProfileJSONFileAndReturnTheDataObject("test/profile_library/wrong_profiles/NotCorrectJSON.json")

    def testPropertyListNotAList(self):
        with self.assertRaises(ValueError):
            validateProfileJSONFileAndReturnTheDataObject("test/profile_library/wrong_profiles/PropertyListNotAList.json")

    def testPropertyListNotContainingDictionaries(self):
        with self.assertRaises(ValueError):
            validateProfileJSONFileAndReturnTheDataObject("test/profile_library/wrong_profiles/PropertyListNotContainingDictionaries.json")

    def testPropertyNotExisting(self):
        with self.assertRaises(ValueError):
            validateProfileJSONFileAndReturnTheDataObject("test/profile_library/wrong_profiles/PropertyNotExisting.json")

    def testSameNamePropertiesWithSameParent(self):
        with self.assertRaises(ValueError):
            validateProfileJSONFileAndReturnTheDataObject("test/profile_library/wrong_profiles/SameNamePropertiesWithSameParent.json")

    def testUnrecognisedKeyword(self):
        with self.assertRaises(ValueError):
            validateProfileJSONFileAndReturnTheDataObject("test/profile_library/wrong_profiles/UnrecognisedKeyword.json")

    def testValueWhenExpectingProperties(self):
        with self.assertRaises(ValueError):
            validateProfileJSONFileAndReturnTheDataObject("test/profile_library/wrong_profiles/ValueWhenExpectingProperties.json")

    def testValueWithoutMatchPattern(self):
        with self.assertRaises(ValueError):
            validateProfileJSONFileAndReturnTheDataObject("test/profile_library/wrong_profiles/ValueWithoutMatchPattern.json")

    def testWrongMarginality(self):
        with self.assertRaises(ValueError):
            validateProfileJSONFileAndReturnTheDataObject("test/profile_library/wrong_profiles/WrongMarginality.json")

    def testWrongMatchPatternType(self):
        with self.assertRaises(ValueError):
            validateProfileJSONFileAndReturnTheDataObject("test/profile_library/wrong_profiles/WrongMatchPatternType.json")

    def testWrongNumberOfRootAttributes(self):
        with self.assertRaises(ValueError):
            validateProfileJSONFileAndReturnTheDataObject("test/profile_library/wrong_profiles/WrongNumberOfRootAttributes.json")

    def testWrongSingleRootAttribute(self):
        with self.assertRaises(ValueError):
            validateProfileJSONFileAndReturnTheDataObject("test/profile_library/wrong_profiles/WrongSingleRootAttribute.json")

    def testWrongValueType(self):
        with self.assertRaises(ValueError):
            validateProfileJSONFileAndReturnTheDataObject("test/profile_library/wrong_profiles/WrongValueType.json")


if __name__ == '__main__':
    unittest.main()
