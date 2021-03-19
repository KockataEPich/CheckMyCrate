import unittest
import src.Classes.CheckCrateType as CCT
import json

class TestCheckCrateType(unittest.TestCase):
    def testWorkflowTypeCrate(self):
        with open("test/sample/ro-crate-metadata.json") as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 

        self.assertTrue(isinstance(CCT.checkIfIndeedWorkflowCrate(crateData), str))

        with open("test/sample/ro-crate-metadata2.json") as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 

        self.assertFalse(isinstance(CCT.checkIfIndeedWorkflowCrate(crateData), str))

    def testDataTypeCrate(self):
        with open("test/sample/ro-crate-metadata2.json") as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 

        self.assertTrue(isinstance(CCT.checkIfIndeedDataCrate(crateData), str))

        with open("test/sample/ro-crate-metadata.json") as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 

        self.assertFalse(isinstance(CCT.checkIfIndeedDataCrate(crateData), str))

if __name__ == '__main__':
    unittest.main()
