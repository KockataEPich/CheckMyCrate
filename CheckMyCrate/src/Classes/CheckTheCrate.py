from   src.Classes.ProfileValidation import ValidateProfileJSONFileAndReturnTheDataObject
from   src.Classes.CratePathAndFileValidation import ValidateCrateJSONFileAndReturnTheDataObject
from   src.Classes.CrateValidation import compareTheCrate
import click

# TODO program when it fact it should coninue. Description needs to be added
# TODO value soma
def checkTheCrate(crate_path, profile_path, writeToFile, verbose):
    global crateData, profileData
    try:
        click.echo("Validating crate integrity...")
        crateData = ValidateCrateJSONFileAndReturnTheDataObject(crate_path)
        click.echo("Crate is OK \n")

        click.echo("Validating profile integrity...")
        profileData = ValidateProfileJSONFileAndReturnTheDataObject(profile_path)
        click.echo("Profile is OK \n")

        click.echo("Validating the profile specification against the crate...")

        validateTheCrateDataAgainstTheProfile(writeToFile)

    except ValueError as e:
        raise ValueError(str(e))









def validateTheCrateDataAgainstTheProfile(writeToFile):
    
    if profileData.get("property_list") == None:
        return
    try:
        validateEntityLoop(crateData.get("./"), profileData)
    except ValueError as e:
        raise ValueError(str(e))


def validateEntity(currentEntity, property):
    
    #checkIfPropertyExistsInEntity(currentEntity, property)
    propertyName = property.get("property")

    #print(propertyName)
    if currentEntity.get(propertyName) == None:
        raise ValueError("Property " + propertyName + " " + property.get("marginality") + 
                         " exist in " + currentEntity.get("@id"))
   
    #print(currentEntity) 
    
    if property.get("property_list") == None:
         return 

    if not isinstance(currentEntity.get(propertyName), dict):
        if crateData.get(currentEntity.get(propertyName)) == None:
            raise ValueError("Property " + propertyName + " is expected to be either a list or a dictionary")
        else:
            validateEntityLoop(crateData.get(currentEntity.get(propertyName)), property)
    else:
        validateEntityLoop(currentEntity.get(propertyName), property)


def validateEntityLoop(entity, property):
   for currentProperty in property.get("property_list"):
        validateEntity(entity, currentProperty)

