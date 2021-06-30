import unittest
from src.Classes.CrateAgainstProfileValidation import compareCrateToProfileSpecification
import os

class TestCrateAgainstProfileValidation(unittest.TestCase):

    def testCorrect(self):
        compareCrateToProfileSpecification("test/crate_library/Correct", 
                                               "test/profile_library/template_profile.json", False)

    def testMissingMustProperties(self):
        with self.assertRaises(ValueError): 
            compareCrateToProfileSpecification("test/crate_library/Correct", 
                                               "test/profile_library/modified_profiles/variaton_one.json", False)

    def testAtLeastAll(self):
        with self.assertRaises(ValueError): 
            compareCrateToProfileSpecification("test/crate_library/Correct", 
                                               "test/profile_library/modified_profiles/variaton_three.json", False)

    def testAtLeastOne(self):
        with self.assertRaises(ValueError): 
            compareCrateToProfileSpecification("test/crate_library/Correct", 
                                               "test/profile_library/modified_profiles/variaton_four.json", False)

    def testAsLiteral(self):
        with self.assertRaises(ValueError): 
            compareCrateToProfileSpecification("test/crate_library/Correct", 
                                               "test/profile_library/modified_profiles/variaton_five.json", False)
    def testExpectedValueTypeNotFound(self):
        with self.assertRaises(ValueError): 
            compareCrateToProfileSpecification("test/crate_library/Correct", 
                                               "test/profile_library/modified_profiles/variaton_six.json", False)

if __name__ == '__main__':
    unittest.main()
