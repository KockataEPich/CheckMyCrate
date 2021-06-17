from src.Classes.ProfileValidation import ValidateProfileJSONFileAndReturnTheDataObject
from os import path
import json

def ValidateCrateJSONFileAndReturnTheDataObject(crate_path):
    try:
        checkIfCratePathLeadsToADirectoryContainingJSONFile(crate_path)
        crateData = validateCrateJSONFileAndReturnTheDataObject(crate_path)
        cradeData = turnTheCrateDataIntoAGraphWithIdsAsKeys(crateData)
        return crateData
    except ValueError as e:
        raise ValueError(str(e))

def checkIfCratePathLeadsToADirectoryContainingJSONFile(crate_path):
    if not path.isdir(crate_path):
        raise ValueError("Invalid RO-Crate path")

    if not path.isfile(crate_path + "/ro-crate-metadata.json") and not path.isfile(crate_path + "/ro-crate-metadata.jsonld"):
        raise ValueError("The directory does not contain the essential \"ro-crate-metadata.json/jsonld\" which means it is not a valid RO-Crate directory")

def validateCrateJSONFileAndReturnTheDataObject(crate_path):
   # Get the actual path to the json
   try:
       json_path = getTheCorrectJsonPath(crate_path)
       return extractDataFromCrateJSONFile(json_path)
   except ValueError as e:
       raise ValueError(str(e))

def getTheCorrectJsonPath(crate_path):
   if path.isfile(crate_path + "/ro-crate-metadata.json"):
        return crate_path + "/ro-crate-metadata.json"
   else:
        return crate_path + "/ro-crate-metadata.jsonld"

def extractDataFromCrateJSONFile(json_path):
    try:
        with open(json_path, 'rb') as json_path:
            return json.load(json_path)
    except Exception as e:
        raise ValueError(str(e))

def turnTheCrateDataIntoAGraphWithIdsAsKeys(crateData):
    crateData = crateData.get("@graph")
    crateGraph = {}
    for item in crateData:
        crateGraph[item.get("@id")] = item

    return crateGraph