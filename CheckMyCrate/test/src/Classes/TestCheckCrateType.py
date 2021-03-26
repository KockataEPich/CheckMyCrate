import unittest
from src.Classes.CheckCrateType import checkCrateType
import json

class TestCheckCrateType(unittest.TestCase):
    def testMissingCrateEntity(self):
        with open("test/sample/different_metadata/crate_id_missing.json") as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 

        crateGraph = {}

        for item in crateData:
            crateGraph[item.get("@id")] = item

        expectedType = "[\"File\", \"SoftwareSourceCode\", \"ComputationalWorkflow\"]"

        self.assertFalse(isinstance(checkCrateType(crateGraph, expectedType, False), str))




    def testMissingMainEntity(self):
        with open("test/sample/different_metadata/missing_main_entity.json") as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 
        crateGraph = {}

        for item in crateData:
            crateGraph[item.get("@id")] = item

        expectedType = "[\"File\", \"SoftwareSourceCode\", \"ComputationalWorkflow\"]"

        self.assertFalse(isinstance(checkCrateType(crateGraph, expectedType, False), str))





    def testMissingMainEntityId(self):
        with open("test/sample/different_metadata/missing_main_entity_id.json") as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 
        crateGraph = {}

        for item in crateData:
            crateGraph[item.get("@id")] = item

        expectedType = "[\"File\", \"SoftwareSourceCode\", \"ComputationalWorkflow\"]"

        self.assertFalse(isinstance(checkCrateType(crateGraph, expectedType, False), str))





    def testMissingMainEntityType(self):
        with open("test/sample/different_metadata/main_entity_missing_type.json") as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 
        crateGraph = {}

        for item in crateData:
            crateGraph[item.get("@id")] = item

        expectedType = "[\"File\", \"SoftwareSourceCode\", \"ComputationalWorkflow\"]"

        self.assertFalse(isinstance(checkCrateType(crateGraph, expectedType, False), str))





    def testCorrect(self):
        
        with open("test/sample/different_metadata/ro-crate-metadata.json") as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 
        crateGraph = {}

        for item in crateData:
            crateGraph[item.get("@id")] = item

        expectedType = "[\"File\", \"SoftwareSourceCode\", \"ComputationalWorkflow\"]"
        
        self.assertTrue(isinstance(checkCrateType(crateGraph, expectedType, False), str))





    def test_Non_Matching_Data(self):
        
        with open("test/sample/different_metadata/ro-crate-metadata.json") as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 
        crateGraph = {}

        for item in crateData:
            crateGraph[item.get("@id")] = item

        expectedType = "Dataset"

        self.assertFalse(isinstance(checkCrateType(crateGraph, expectedType, False), str))





if __name__ == '__main__':
    unittest.main()
