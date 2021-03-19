# Stop the program if the paths are no specified properly
import src.Classes.Viability as Viability
import src.Classes.CheckCrateType as CCT
import src.Classes.CrateValidation as CV
import json
import os.path

def checkTheCrate(crate_path, profile_path):
    if not Viability.isItViable(crate_path, profile_path):
       return False
       
    if os.path.isfile(crate_path + "/ro-crate-metadata.json") == True:
        json_path = crate_path + "/ro-crate-metadata.json"
    else:
        json_path = crate_path + "/ro-crate-metadata.jsonld"


    with open(json_path) as json_path:
        crateData = json.load(json_path)

    crateData = crateData.get("@graph") 

    with open(profile_path, 'rb') as profile_path:
        profileData = json.loads(profile_path.read().decode("utf-8","ignore"))
    
    mainEntityId = CCT.checkCrateType(crateData, json.dumps(profileData.get("main_entity_type")))

    
    if isinstance(mainEntityId, int):
        return False

    crateGraph = {}

    for item in crateData:
        crateGraph[item.get("@id")] = item


    crateId = "./"

    # JSON arrays with their respective cardinality
    minimumMarginalityArray = profileData["properties"][0]["minimum"]
    recommendedMarginalityArray = profileData["properties"][1]["recommended"]
    optionaMarginalityArray = profileData["properties"][2]["optional"]

    if os.path.isfile("output.txt") == True:
        os.remove("output.txt")

    isItOkay = CV.compareTheCrate(minimumMarginalityArray, crateGraph, crateId, mainEntityId, "MUST")
    CV.compareTheCrate(recommendedMarginalityArray, crateGraph, crateId, mainEntityId, "SHOULD")
    CV.compareTheCrate(optionaMarginalityArray, crateGraph, crateId, mainEntityId, "COULD")

    return isItOkay
