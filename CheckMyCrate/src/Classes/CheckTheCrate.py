from   src.Classes.ProfileValidation import ValidateProfileJSONFileAndReturnTheDataObject
from   src.Classes.CrateValidation import ValidateCrateJSONFileAndReturnTheDataObject
import traceback
import click
import json

# TODO program when it fact it should coninue. Description needs to be added
# TODO value soma
# TODO cardinality
def checkTheCrate(crate_path, profile_path, writeToFile, verbose):
    global crateData, profileData, shouldWrite
    shouldWrite = writeToFile
    try:
        click.echo("Validating crate integrity...")
        crateData = ValidateCrateJSONFileAndReturnTheDataObject(crate_path)
        click.echo("Crate is OK \n")

        click.echo("Validating profile integrity...")
        profileData = ValidateProfileJSONFileAndReturnTheDataObject(profile_path)
        click.echo("Profile is OK \n")

        click.echo("Validating the profile specification against the crate...")

        validateEntityLoop(crateData.get("./"), profileData)

    except ValueError as e:
        traceback.print_exc()
        raise ValueError(e)



def validateEntityLoop(entity, property):
    if property.get("property_list") == None:
        return

    for currentProperty in property.get("property_list"):
        validateEntity(entity, currentProperty)



def validateEntity(currentEntity, property):
    ensurePropertyExistsInEntity(currentEntity, property)
    ensureValueIsCorrectIfApplicable(currentEntity, property)
    ensureCardinalitIsCorrectIfApplicable(currentEntity, property)
    checkIfPropertyHasSubPropertiesAndLoopIfItDoes(currentEntity, property)

  

def ensurePropertyExistsInEntity(currentEntity, property):
    if currentEntity.get(property.get("property")) == None:
        raise ValueError("Property " + property.get("property") + " " + property.get("marginality") + 
                         " exist in " + currentEntity.get("@id"))



def ensureValueIsCorrectIfApplicable(currentEntity, property):
    if property.get("expected_value") == None:
        return
    
    if isinstance(currentEntity.get(property.get("property")), dict):
        raise ValueError("Value of property " + property.get("property") + " is NOT expected to be a dictionary")

    doMatch_PatternValueCheck(currentEntity, property)



def ensureCardinalitIsCorrectIfApplicable(currentEntity, property):
    if property.get("cardinality") == None:
        return

    if property.get("cardinality") == "ONE" and isinstance(currentEntity.get(property.get("property")), list):
        raise ValueError("Value of property " + property.get("property") + " cannot be a list since the cardinality " + 
                         "in the profile file is \"ONE\"")
    


def checkIfPropertyHasSubPropertiesAndLoopIfItDoes(currentEntity, property):
    if property.get("property_list") == None:
        return 

    if isinstance(currentEntity.get(property.get("property")), dict):
        validateEntityLoop(currentEntity.get(property.get("property")), property)
        return

    if isinstance(currentEntity.get(property.get("property")), list):
        raise ValueError("Value of property " + property.get("property") + " cannot be a list")
        
    newEntity = crateData.get(currentEntity.get(property.get("property")))

    if newEntity == None:
        raise ValueError("If Value of property " + property.get("property") + " is not a dictionary, then it MUST" +
                         " point to an entity in the array")

    validateEntityLoop(newEntity, property)



        


def doNormalValueCheck(expected_value, actual_value, propertyName):
    
    expectedValue = json.dumps(expected_value)
    actualValue = json.dumps(actual_value)
    
    if expectedValue.find(actualValue) == -1:
        raise ValueError("Value of property \"" + propertyName + "\" is " + actualValue + " but MUST be " + expectedValue)


def doMatch_PatternValueCheck(currentEntity, property):
    match_pattern = property.get("match_pattern")
    actualValue = currentEntity.get(property.get("property"))
    expectedValue = property.get("expected_value")

    if match_pattern == "at_least_one":
        for item in expectedValue:
            if item in actualValue:
                return
        else:
             raise ValueError("Value of property \"" + property.get("property") + 
                              "\" is " + json.dumps(actualValue) + " but it MUST contain at least one of "
                              + json.dumps(expectedValue))

    if match_pattern == "as_literal" :
        doNormalValueCheck(expectedValue, actualValue, property.get("property"))
        return

    if match_pattern == "at_least_all":
        for item in expectedValue:
            if item not in actualValue:
                 raise ValueError("Value of property \"" + property.get("property") + "\" is " + json.dumps(actualValue) + 
                                  " but it MUST have all the entities in " + json.dumps(expectedValue))