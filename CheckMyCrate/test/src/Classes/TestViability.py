import unittest
import src.Classes.Viability as V

class TestViability(unittest.TestCase):
    def testViability(self):
        self.assertTrue(V.isItViable("test/sample/", "test/profile_library/ro_crate_1.1_basic.json"))
        self.assertFalse(V.isItViable("test/sample/", "file_non_existent"))
        self.assertFalse(V.isItViable("file_non_existent", "test/profile_library/ro_crate_1.1_basic.json"))
      
        
if __name__ == '__main__':
    unittest.main()
