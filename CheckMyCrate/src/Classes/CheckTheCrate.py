# Stop the program if the paths are no specified properly
import src.Classes.Viability as Viability
import src.Classes.CrateChecks as CC
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


    with open(profile_path) as profile_path:
        profileData = json.load(profile_path)

    resolution = False

    if profileData["@type"] == "WorkflowCrate":
        resolution = CC.checkWorkflowCrates(crateData, profileData)
    else:
        resolution = CC.checkDataCrates(crateData, profileData)

    return resolution
