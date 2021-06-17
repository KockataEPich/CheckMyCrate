from   src.Classes.Viability import isItViable
from   src.Classes.CheckCrateType import checkCrateType
from   src.Classes.CrateValidation import compareTheCrate
import json
import os.path
import click


# Method that invokes all other methods in order to achieve the desired functionality
# Inputs are the crate path, profile path, flag for writing to a file and 
# if the verbose in case type does not match
# Output is a boolean depending which indicated if the everything is OK or not 
def checkTheCrate(crate_path, profile_path, writeToFile, verbose):
    click.echo("Validating profile and crate file's integrity...")

    # Checking if the the two paths are viable crate and profile paths
    # isItViable returns a list where the first item is the prepared
    # crate data while the second one is the prepared profile data
   # try:
    #    crateAndProfileData = isItViable(crate_path, profile_path)
    #except:

    crateAndProfileData = isItViable(crate_path, profile_path)
    
    # isItViable returns a bool False if there is a problem. Otherwise it returns the crateData
    if isinstance(crateAndProfileData, bool):
       return False
     
    click.echo("Profile and crate are viable files!\n")



    click.echo("Validating the main entity of the crate...")
    # Check the crate type
    mainEntityId = checkCrateType(crateAndProfileData[0], json.dumps(
                    crateAndProfileData[1].get("main_entity_type")), verbose)

    # checkCrateType returns a False if there is a problem
    if not mainEntityId:
        return False

    click.echo("Crate has valid main entity!\n")


    click.echo("Validating the profile specification against the crate...")
    
    crateId = "./"

    # JSON arrays with their respective cardinalities
    minimumArray = crateAndProfileData[1]["properties"][0]["minimum"]
    recommendedArray = crateAndProfileData[1]["properties"][1]["recommended"]
    optionalArray = crateAndProfileData[1]["properties"][2]["optional"]

    # Check if the last output.txt file exists and if it does delete it
    if os.path.isfile("output.txt") and writeToFile:
        os.remove("output.txt")

    
    # Check each array. compareTheCrate returns 1 if everything is OK, 0 if there is a missing entity
    # and -1 if the entity is present, but incorrectly used
    isItOkayMin = compareTheCrate(minimumArray, crateAndProfileData[0], crateId, mainEntityId, "MUST", writeToFile) == 1
    isItOkayRec = compareTheCrate(recommendedArray, crateAndProfileData[0], crateId, mainEntityId, "SHOULD", writeToFile) != -1
    isItOkayOpt = compareTheCrate(optionalArray, crateAndProfileData[0], crateId, mainEntityId, "COULD", writeToFile) != -1

    return isItOkayMin and isItOkayRec and isItOkayOpt




