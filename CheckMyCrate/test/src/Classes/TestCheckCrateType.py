import unittest
from src.Classes.CheckCrateType import checkCrateType
import json

class TestCheckCrateType(unittest.TestCase):
    def testMissingCrateEntity(self):
        with open("test/sample/different_metadata/crate_id_missing.json") as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 
        expectedType = "[\"File\", \"SoftwareSourceCode\", \"ComputationalWorkflow\"]"

        self.assertFalse(isinstance(checkCrateType(crateData, expectedType), str))

    def testMissingMainEntity(self):
        with open("test/sample/different_metadata/missing_main_entity.json") as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 
        expectedType = "[\"File\", \"SoftwareSourceCode\", \"ComputationalWorkflow\"]"

        self.assertFalse(isinstance(checkCrateType(crateData, expectedType), str))

    def testMissingMainEntityId(self):
        with open("test/sample/different_metadata/missing_main_entity_id.json") as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 
        expectedType = "[\"File\", \"SoftwareSourceCode\", \"ComputationalWorkflow\"]"

        self.assertFalse(isinstance(checkCrateType(crateData, expectedType), str))

    def testMissingMainEntityType(self):
        with open("test/sample/different_metadata/main_entity_missing_type.json") as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 
        expectedType = "[\"File\", \"SoftwareSourceCode\", \"ComputationalWorkflow\"]"

        self.assertFalse(isinstance(checkCrateType(crateData, expectedType), str))

    def testCorrect(self):
        
        with open("test/sample/different_metadata/ro-crate-metadata.json") as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 
        expectedType = "[\"File\", \"SoftwareSourceCode\", \"ComputationalWorkflow\"]"
        
        self.assertTrue(isinstance(checkCrateType(crateData, expectedType), str))

    def test_Non_Matching_Data(self):
        
        with open("test/sample/different_metadata/ro-crate-metadata.json") as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 
        expectedType = "Dataset"

        self.assertFalse(isinstance(checkCrateType(crateData, expectedType), str))


if __name__ == '__main__':
    unittest.main()
