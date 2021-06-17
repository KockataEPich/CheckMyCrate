from   src.Classes.ProfileValidation import ValidateProfileJSONFileAndReturnTheDataObject
from   src.Classes.CratePathAndFileValidation import ValidateCrateJSONFileAndReturnTheDataObject
from   src.Classes.CrateValidation import compareTheCrate
import click

def checkTheCrate(crate_path, profile_path, writeToFile, verbose):
    try:
        click.echo("Validating profile and crate file's integrity...")

        crateData = ValidateCrateJSONFileAndReturnTheDataObject(crate_path)
        profileData = ValidateProfileJSONFileAndReturnTheDataObject(profile_path)

        click.echo("Profile and crate are viable files!\n")
        click.echo("Validating the profile specification against the crate...")

        validateTheCrateDataAgainstTheProfile(crateData, profileData, writeToFile)

    except ValueError as e:
        raise ValueError(str(e))

def validateTheCrateDataAgainstTheProfile(crateData, profileData, writeToFile):
    
    if profileData.get("property_list") == None:
        return

    startingEntity = crateData.get("./")

    for property in profileData.get("property_list"):
        validateEntity(startingEntity, property)

def validateEnttiy(currentEntity, property):
    if currentEntity.get(property.get("property")) == None:
        # TODO Marginality needs to be implemented. This also stops the program when it fact it should coninue. Description needs to be added
        raise ValueError("Property " + property.get("property") + " does not exist in " + currentEntity.get("@id"))

    #if property.get("expected_value") != None 

    # TODO this needs to check if the value points to something else in the graph
    if property.get("property_list") != None and not isinstance(currentEntity.get(property.get("property")), dict) and not isinstance(currentEntity.get(property.get("property")), list):
        #checkIfValuePointsToSomethingInArray()
        raise ValueError("Property " + property.get("property") + " is expected to be either a list or a dictionary")


       
    #crateId = "./"

    ## JSON arrays with their respective cardinalities
    #minimumArray = crateAndProfileData[1]["properties"][0]["minimum"]
    #recommendedArray = crateAndProfileData[1]["properties"][1]["recommended"]
    #optionalArray = crateAndProfileData[1]["properties"][2]["optional"]

    ## Check if the last output.txt file exists and if it does delete it
    #if os.path.isfile("output.txt") and writeToFile:
    #    os.remove("output.txt")

    
    ## Check each array. compareTheCrate returns 1 if everything is OK, 0 if there is a missing entity
    ## and -1 if the entity is present, but incorrectly used
    #isItOkayMin = compareTheCrate(minimumArray, crateAndProfileData[0], crateId, mainEntityId, "MUST", writeToFile) == 1
    #isItOkayRec = compareTheCrate(recommendedArray, crateAndProfileData[0], crateId, mainEntityId, "SHOULD", writeToFile) != -1
    #isItOkayOpt = compareTheCrate(optionalArray, crateAndProfileData[0], crateId, mainEntityId, "COULD", writeToFile) != -1

    #return isItOkayMin and isItOkayRec and isItOkayOpt




