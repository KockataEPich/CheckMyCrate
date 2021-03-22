import unittest
import src.Classes.Viability as V

class TestViability(unittest.TestCase):
    def testCorrect(self):
        self.assertTrue(V.isItViable("test/sample/", "test/profile_library/ro_crate_1.1_basic.json"))

    def testNonExistentProfile(self):
        self.assertFalse(V.isItViable("test/sample/", "file_non_existent"))

    def testNonExistentCrate(self):
        self.assertFalse(V.isItViable("file_non_existent", "test/profile_library/ro_crate_1.1_basic.json"))

    def testNonOKProfile(self):
        self.assertFalse(V.isItViable("test/sample/", "test/profile_library/wrong_profiles/wrongProfile1.json"))

    def testNonOKJsonProfileFile(self):
        self.assertFalse(V.isItViable("test/sample/", "test/profile_library/wrong_profiles/wrongProfile19.json"))

    def testNonOkJsonCrateFile(self):
        self.assertFalse(V.isItViable("test/sample/wrong_metadata/", "test/profile_library/ro_crate_1.1_basic.json"))

        
        
        
        
        
if __name__ == '__main__':
    unittest.main()
