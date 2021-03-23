import unittest
import json
import src.Classes.CrateValidation as CV
class TestCrateValidation(unittest.TestCase):
    def testCorrect(self):

        with open("test/sample/different_metadata/ro-crate-metadata.json", 'rb') as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 

        crateGraph = {}

        for item in crateData:
            crateGraph[item.get("@id")] = item

        array = [ 
                 {
                    "@id": "license",
                    "expected_type": [ "CreativeWork", "URL" ],
                    "description": "The license of the crate",
                    "cardinality": "MANY"
                 },
                 {
                    "@id": "sdPublisher",
                    "expected_type": [
                        "Organization",
                        "Person"
                    ],
                    "description": "The publisher",
                    "cardinality": "MANY"
                }
        ]

        self.assertEquals(CV.compareTheCrate(array,crateGraph,"./","Galaxy-Workflow-MC_COVID19like_Assembly_Reads.ga", "MUST", False), 1)


    def testNoFind(self):

        with open("test/sample/different_metadata/ro-crate-metadata.json", 'rb') as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 

        crateGraph = {}

        for item in crateData:
            crateGraph[item.get("@id")] = item

        array = [ 
                 {
                    "@id": "licenseNot",
                    "expected_type": [ "CreativeWork", "URL" ],
                    "description": "The license of the crate",
                    "cardinality": "MANY"
                 },
                 {
                    "@id": "sdPublisher",
                    "expected_type": [
                        "Organization",
                        "Person"
                    ],
                    "description": "The publisher",
                    "cardinality": "MANY"
                }]

        self.assertEquals(CV.compareTheCrate(array,crateGraph,"./","Galaxy-Workflow-MC_COVID19like_Assembly_Reads.ga", "MUST", False), 0)


    def testNoMatchingTypes(self):

        with open("test/sample/different_metadata/ro-crate-metadata.json", 'rb') as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 

        crateGraph = {}

        for item in crateData:
            crateGraph[item.get("@id")] = item

        array = [ 
                 {
                    "@id": "license",
                    "expected_type": [ "CreativeWork", "URL" ],
                    "description": "The license of the crate",
                    "cardinality": "MANY"
                 },
                 {
                    "@id": "sdPublisher",
                    "expected_type": [
                        "Organisation",
                        "PersonNotPerson"
                    ],
                    "description": "The publisher",
                    "cardinality": "MANY"
                }]

        self.assertEquals(CV.compareTheCrate(array,crateGraph,"./","Galaxy-Workflow-MC_COVID19like_Assembly_Reads.ga", "MUST", False), -1)

    def testWrongCardinality(self):

        with open("test/sample/different_metadata/ro-crate-metadata.json", 'rb') as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 

        crateGraph = {}

        for item in crateData:
            crateGraph[item.get("@id")] = item

        array = [ 
                 {
                    "@id": "license",
                    "expected_type": [ "CreativeWork", "URL" ],
                    "description": "The license of the crate",
                    "cardinality": "MANY"
                 },
                 {
                    "@id": "hasPart",
                    "expected_type": "CreativeWork",
                    "description": "Indicates an item or CreativeWork that is part of this item, or CreativeWork (in some sense). Inverse property: isPartOf.",
                    "cardinality": "ONE"
                }]

        self.assertEquals(CV.compareTheCrate(array,crateGraph,"./","Galaxy-Workflow-MC_COVID19like_Assembly_Reads.ga", "MUST", False), -1)

    def testMissingTypeInReferencedItem(self):

        with open("test/sample/different_metadata/main_entity_missing_type.json", 'rb') as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 

        crateGraph = {}

        for item in crateData:
            crateGraph[item.get("@id")] = item

        array = [ 
                 {
                    "@id": "license",
                    "expected_type": [ "CreativeWork", "URL" ],
                    "description": "The license of the crate",
                    "cardinality": "MANY"
                 },
                {
                    "@id": "sdPublisher",
                    "expected_type": [
                        "Organisation",
                        "Person"
                    ],
                    "description": "The publisher",
                    "cardinality": "MANY"
                }]

        self.assertEquals(CV.compareTheCrate(array,crateGraph,"./","Galaxy-Workflow-MC_COVID19like_Assembly_Reads.ga", "MUST", False), -1)


    def testMissingItemInGraph(self):

        with open("test/sample/different_metadata/item_missing_in_graph.json", 'rb') as json_path:
            crateData = json.load(json_path)

        crateData = crateData.get("@graph") 

        crateGraph = {}

        for item in crateData:
            crateGraph[item.get("@id")] = item

        array = [ 
                 {
                    "@id": "license",
                    "expected_type": [ "CreativeWork", "URL" ],
                    "description": "The license of the crate",
                    "cardinality": "MANY"
                 },
                {
                    "@id": "sdPublisher",
                    "expected_type": [
                        "Organisation",
                        "Person"
                    ],
                    "description": "The publisher",
                    "cardinality": "MANY"
                }]

        self.assertEquals(CV.compareTheCrate(array,crateGraph,"./","Galaxy-Workflow-MC_COVID19like_Assembly_Reads.ga", "MUST", False), -1)

if __name__ == '__main__':
    unittest.main()
