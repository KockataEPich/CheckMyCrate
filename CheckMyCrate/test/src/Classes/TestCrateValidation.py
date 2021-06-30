import unittest
import json
from src.Classes.CrateValidation import validateCrateJSONFileAndReturnTheDataObject
class TestCrateValidation(unittest.TestCase):
    def testCorrect(self):
        validateCrateJSONFileAndReturnTheDataObject("test/crate_library/Correct")



    def testWrongJSON(self):
        with self.assertRaises(ValueError):
            validateCrateJSONFileAndReturnTheDataObject("test/crate_library/WrongJSON")



    def testNoGraph(self):
        with self.assertRaises(ValueError):
            validateCrateJSONFileAndReturnTheDataObject("test/crate_library/NoGraph")
   
    def testGraphNotAList(self):
        with self.assertRaises(ValueError):
            validateCrateJSONFileAndReturnTheDataObject("test/crate_library/GraphNotAList")

    def testNoCrateId(self):
        with self.assertRaises(ValueError):
            validateCrateJSONFileAndReturnTheDataObject("test/crate_library/NoCrateId")

    def testIncorrectCrateIdValue(self):
        with self.assertRaises(ValueError):
            validateCrateJSONFileAndReturnTheDataObject("test/crate_library/IncorrectCrateIdValue")
    
if __name__ == '__main__':
    unittest.main()
