# Stop the program if the paths are no specified properly
from   src.Classes.Viability import isItViable
from   src.Classes.CheckCrateType import checkCrateType
from   src.Classes.CrateValidation import compareTheCrate
import json
import os.path
import click

def checkTheCrate(crate_path, profile_path, writeToFile):
    click.echo("Validating profile and crate file's integrity...")

    crateData = isItViable(crate_path, profile_path)
    if isinstance(crateData, bool):
       return False
       
    click.echo("Profile and crate are viable files!\n")

    crateData = crateData.get("@graph") 

    with open(profile_path, 'rb') as profile_path:
        profileData = json.loads(profile_path.read().decode("utf-8","ignore"))
    
    click.echo("Validating the main entity of the crate...")
    mainEntityId = checkCrateType(crateData, json.dumps(profileData.get("main_entity_type")))

    
    if isinstance(mainEntityId, int):
        return False

    click.echo("Crate has valid main entity!\n")

    crateGraph = {}

    for item in crateData:
        crateGraph[item.get("@id")] = item


    crateId = "./"

    click.echo("Validating the profile specification against the crate...")
    # JSON arrays with their respective cardinality
    minimumMarginalityArray = profileData["properties"][0]["minimum"]
    recommendedMarginalityArray = profileData["properties"][1]["recommended"]
    optionaMarginalityArray = profileData["properties"][2]["optional"]

    if os.path.isfile("output.txt") and writeToFile:
        os.remove("output.txt")

    isItOkay = True

    if compareTheCrate(minimumMarginalityArray, crateGraph, crateId, mainEntityId, "MUST", writeToFile) < 1:
        isItOkay = False

    if compareTheCrate(recommendedMarginalityArray, crateGraph, crateId, mainEntityId, "SHOULD", writeToFile) == -1:
        isItOkay = False

    if compareTheCrate(optionaMarginalityArray, crateGraph, crateId, mainEntityId, "COULD", writeToFile) == -1:
        isItOkay = False

    return isItOkay
